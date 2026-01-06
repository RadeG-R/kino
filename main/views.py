# main/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from collections import defaultdict
import datetime
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model, login

import qrcode
import qrcode.image.svg
from io import BytesIO
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth.views import LoginView as BaseLoginView

from .models import Film, Seans, Rezerwacja, Profil, LoginAttempt, Recenzja
from .forms import RejestracjaForm, LogowanieForm, UserUpdateForm, ProfilForm, UproszczonyOTPForm, RecenzjaForm
from .utils import is_admin_by_username


class CustomLoginView(LoginView):
    form_class = LogowanieForm
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.POST.get('username') or self.request.GET.get('username', '')
        if username:
            attempt = LoginAttempt.objects.filter(username=username).first()
            if attempt and attempt.is_locked and attempt.lock_until:
                remaining = int((attempt.lock_until - timezone.now()).total_seconds())
                if remaining > 0:
                    context['is_locked'] = True
                    context['remaining_seconds'] = remaining
                    context['failures'] = attempt.failures
        return context

    def dispatch(self, request, *args, **kwargs):
        username = request.POST.get('username') or request.GET.get('username', '')
        # Używamy filter().first() zamiast get_or_create, aby uniknąć tworzenia pustych wpisów
        attempt = LoginAttempt.objects.filter(username=username).first()

        if attempt and attempt.is_locked:
            if attempt.lock_until and timezone.now() < attempt.lock_until:
                # Nie robimy redirectu tutaj, pozwalamy get_context_data wyświetlić licznik
                pass
            elif attempt.failures >= 15:
                messages.error(request, 'Konto permanentnie zablokowane. Skontaktuj się z administratorem.')
                # Nie robimy redirectu, pozwalamy na wyświetlenie strony
            else:
                # Blokada czasowa minęła
                attempt.is_locked = False
                attempt.save()

        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        username = form.data.get('username')

        # Ignorujemy całkowicie adminów
        if is_admin_by_username(username):
            return super().form_invalid(form)

        attempt, created = LoginAttempt.objects.get_or_create(username=username)
        attempt.failures += 1

        if attempt.failures >= 15:
            attempt.is_locked = True
            attempt.lock_until = None
            messages.error(self.request,
                           'Konto permanentnie zablokowane po 15 nieudanych próbach. Skontaktuj się z administratorem.')
        elif attempt.failures >= 5:
            lock_duration = 30 * (attempt.failures - 4)
            attempt.is_locked = True
            attempt.lock_until = timezone.now() + timezone.timedelta(seconds=lock_duration)
            messages.error(self.request, 'Zbyt wiele nieudanych prób. Konto zablokowane.', extra_tags='lockout')
        else:
            messages.error(self.request, f'Nieprawidłowe dane logowania. Pozostało {5 - attempt.failures} prób.')

        attempt.save()
        return super().form_invalid(form)

    # OSTATECZNA POPRAWKA JEST TUTAJ
    def form_valid(self, form):
        user = form.get_user()

        # POBIERAMY OBIEKT 'attempt' ZANIM GO UŻYJEMY
        attempt = LoginAttempt.objects.filter(username=user.username).first()
        if attempt:
            attempt.failures = 0
            attempt.is_locked = False
            attempt.lock_until = None
            attempt.save()

        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()

        if device:
            from django.contrib.auth import logout
            logout(self.request)
            self.request.session['otp_user_id'] = user.id
            return redirect('otp_login')
        else:
            # Używamy wbudowanej funkcji login, aby poprawnie zalogować użytkownika
            login(self.request, user)
            # Zwracamy odpowiedź z nadklasy, która obsłuży przekierowanie
            return super().form_valid(form)


# ... (reszta pliku views.py, która jest poprawna, zostaje bez zmian) ...
# Poniżej wklejam resztę dla kompletności

class CustomOTPLoginView(BaseLoginView):
    template_name = 'registration/otp_login.html'
    form_class = UproszczonyOTPForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user_id = self.request.session.get('otp_user_id')
        if user_id:
            User = get_user_model()
            try:
                kwargs['user'] = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                pass
        return kwargs

    def form_valid(self, form):
        user_to_login = form.user
        attempt = LoginAttempt.objects.filter(username=user_to_login.username).first()
        if attempt:
            attempt.failures = 0
            attempt.is_locked = False
            attempt.lock_until = None
            attempt.save()
        login(self.request, user_to_login, backend='main.backends.EmailOrUsernameBackend')
        if 'otp_user_id' in self.request.session:
            del self.request.session['otp_user_id']
        return redirect(self.get_success_url())


class RejestracjaView(CreateView):
    form_class = RejestracjaForm
    success_url = reverse_lazy('login')
    template_name = 'registration/rejestracja.html'


@method_decorator(login_required, name='dispatch')
class Setup2FAView(TemplateView):
    template_name = 'konto/2fa_setup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()
        if not device:
            device = TOTPDevice.objects.filter(user=user).first() or TOTPDevice.objects.create(user=user,
                                                                                               confirmed=False)
            qr_uri = device.config_url
            img_factory = qrcode.image.svg.SvgPathImage
            qr_img = qrcode.make(qr_uri, image_factory=img_factory)
            stream = BytesIO()
            qr_img.save(stream)
            context['qr_code'] = stream.getvalue().decode()
        context['device'] = device
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        device = TOTPDevice.objects.filter(user=user).first()
        if 'disable_2fa' in request.POST:
            if device and device.confirmed:
                token = request.POST.get('disable_token')
                try:
                    if device.verify_token(int(token)):
                        device.delete()
                        messages.success(request, 'Weryfikacja dwuetapowa została wyłączona.')
                        return redirect('konto')
                    else:
                        messages.error(request, 'Nieprawidłowy kod OTP. Nie można wyłączyć 2FA.')
                except (ValueError, TypeError):
                    messages.error(request, 'Proszę wpisać prawidłowy kod.')
            return redirect('2fa_setup')
        token = request.POST.get('token')
        try:
            if device and device.verify_token(int(token)):
                device.confirmed = True
                device.save()
                messages.success(request, 'Weryfikacja dwuetapowa została pomyślnie aktywowana.')
                return redirect('konto')
        except (ValueError, TypeError):
            pass
        messages.error(request, 'Nieprawidłowy kod. Spróbuj ponownie.')
        return redirect('2fa_setup')


class IndexView(ListView):
    model = Film
    template_name = 'index.html'
    context_object_name = 'filmy_w_kinie'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_filmy = Film.objects.all()
        filmy_oceniane = sorted(all_filmy, key=lambda f: f.srednia_ocena(), reverse=True)[:3]
        context['top_rated_filmy'] = filmy_oceniane
        seanse_nadchodzace = Seans.objects.filter(data_i_godzina__gte=timezone.now()).order_by('data_i_godzina')[:5]
        context['upcoming_seanse'] = seanse_nadchodzace
        return context


class FilmyView(ListView):
    model = Film
    template_name = "filmy.html"
    context_object_name = 'lista_filmow'
    paginate_by = 9


class FilmDetailView(FormMixin, DetailView):
    model = Film
    template_name = "film.html"
    context_object_name = 'film'
    form_class = RecenzjaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        film = self.get_object()
        context['recenzje'] = film.recenzje.all().order_by('-data_dodania')
        seanse_filmu = Seans.objects.filter(film=film, data_i_godzina__gte=timezone.now()).order_by('data_i_godzina')
        context['seanse_filmu'] = seanse_filmu
        if self.request.user.is_authenticated:
            existing = film.recenzje.filter(uzytkownik=self.request.user).first()
            context['form'] = RecenzjaForm(instance=existing) if existing else RecenzjaForm()
            context['existing_recenzja'] = existing
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect('login')
        existing = self.object.recenzje.filter(uzytkownik=request.user).first()
        form = RecenzjaForm(request.POST, instance=existing) if existing else RecenzjaForm(request.POST)
        if form.is_valid():
            recenzja = form.save(commit=False)
            recenzja.film = self.object
            recenzja.uzytkownik = request.user
            recenzja.save()
            messages.success(request, 'Recenzja została dodana/zaktualizowana.')
            return redirect('film-detail', pk=self.object.pk)
        else:
            messages.error(request, 'Błąd w formularzu recenzji.')
            return self.render_to_response(self.get_context_data(form=form))


class SeanseView(TemplateView):
    template_name = 'seanse.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year, month, day = self.kwargs.get('year'), self.kwargs.get('month'), self.kwargs.get('day')
        wybrana_data = datetime.date(year, month, day) if year and month and day else timezone.now().date()
        context['wybrana_data'] = wybrana_data
        context['lista_dni'] = [wybrana_data + datetime.timedelta(days=i) for i in range(7)]
        seanse = Seans.objects.filter(data_i_godzina__date=wybrana_data).order_by('data_i_godzina').select_related(
            'film')
        pogrupowane_seanse = defaultdict(list)
        for seans in seanse:
            pogrupowane_seanse[seans.film].append(seans)
        context['pogrupowane_seanse'] = dict(pogrupowane_seanse)
        return context


class RezerwacjaView(LoginRequiredMixin, TemplateView):
    template_name = 'rezerwacja.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seans = get_object_or_404(Seans, pk=self.kwargs['seans_id'])
        context['seans'] = seans
        zajete_miejsca_qs = Rezerwacja.objects.filter(seans=seans).values_list('miejsca', flat=True)
        zajete_miejsca = [miejsce for miejsca_str in zajete_miejsca_qs for miejsce in miejsca_str.split(',')]
        context['zajete_miejsca'] = zajete_miejsca
        context['rzedy'] = [chr(65 + i) for i in range(6)]
        context['miejsca_w_rzedzie'] = range(1, 13)
        return context

    def post(self, request, *args, **kwargs):
        seans = get_object_or_404(Seans, pk=self.kwargs['seans_id'])
        miejsca_str = request.POST.get('miejsca', '')
        lista_miejsc = [miejsce for miejsce in miejsca_str.split(',') if miejsce]
        if lista_miejsc:
            Rezerwacja.objects.create(uzytkownik=request.user, seans=seans, miejsca=",".join(lista_miejsc))
            return redirect('konto')
        return redirect('rezerwacja', seans_id=seans.id)


class KontoView(LoginRequiredMixin, ListView):
    model = Rezerwacja
    template_name = 'konto.html'
    context_object_name = 'moje_rezerwacje'

    def get_queryset(self):
        return Rezerwacja.objects.filter(uzytkownik=self.request.user).order_by('-data_rezerwacji')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['moje_recenzje'] = Recenzja.objects.filter(uzytkownik=self.request.user).select_related('film')
        return context


class AdminView(TemplateView):
    template_name = "admin.html"


class InfoView(TemplateView):
    template_name = "info.html"


class KontaktView(TemplateView):
    template_name = "kontakt.html"


class FAQView(TemplateView):
    template_name = "faq.html"


class PolitykaPrywatnosciView(TemplateView):
    template_name = "polityka_prywatnosci.html"


class RegulaminView(TemplateView):
    template_name = "regulamin.html"


class CookiesView(TemplateView):
    template_name = "cookies.html"


@login_required
def edytuj_profil(request):
    profil_obj, created = Profil.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfilForm(request.POST, request.FILES, instance=profil_obj)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, 'Profil został zaktualizowany.')
            return redirect('konto')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfilForm(instance=profil_obj)
    return render(request, 'edytuj_profil.html', {'form': uform, 'pform': pform})