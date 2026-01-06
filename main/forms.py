from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import User
from django_recaptcha.fields import ReCaptchaField
import re

from .models import Profil, Recenzja, Recenzja

class LogowanieForm(AuthenticationForm):
    username = forms.CharField(label="Nazwa użytkownika lub e-mail", widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label="Hasło", strip=False, widget=forms.PasswordInput)
    captcha = ReCaptchaField(label='')


class RejestracjaForm(UserCreationForm):
    username = forms.CharField(label="Nazwa użytkownika")
    email = forms.EmailField(label="Adres e-mail", required=True, help_text="Wymagane. Podaj poprawny adres email.")
    password1 = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Potwierdź hasło", widget=forms.PasswordInput)
    captcha = ReCaptchaField(label='')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Użytkownik z tym adresem e-mail już istnieje.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise forms.ValidationError("Hasło musi zawierać co najmniej 8 znaków, jedną dużą literę, jedną cyfrę i jeden znak specjalny.")
        return password


class AdminCaptchaForm(AdminAuthenticationForm):
    captcha = ReCaptchaField(label='')

class UproszczonyOTPForm(forms.Form):
    otp_token = forms.CharField(
        label="6-cyfrowy kod weryfikacyjny",
        max_length=6,
        widget=forms.TextInput(attrs={'autocomplete': 'off', 'autofocus': True})
    )

    def __init__(self, user, request=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_otp_token(self):
        token = self.cleaned_data.get('otp_token')

        if not token or not token.isdigit():
            raise forms.ValidationError("Wpisz poprawny, 6-cyfrowy kod.")

        try:
            token_int = int(token)
        except (ValueError, TypeError):
            raise forms.ValidationError("Nieprawidłowy format kodu.")

        device = self.user.totpdevice_set.filter(confirmed=True).first()

        if not device or not device.verify_token(token_int):
            raise forms.ValidationError("Nieprawidłowy kod weryfikacyjny. Spróbuj ponownie.")

        return token

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class RecenzjaForm(forms.ModelForm):
    ocena = forms.FloatField(widget=forms.HiddenInput(), min_value=0.5, max_value=5.0)

    class Meta:
        model = Recenzja
        fields = ['ocena', 'tresc']
        widgets = {
            'tresc': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Napisz swoją recenzję...'}),
        }


class ProfilForm(forms.ModelForm):
    class Meta:
        model = Profil
        fields = ['avatar']