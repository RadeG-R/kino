from django.contrib import admin
from .models import Film, Seans, Rezerwacja, LoginAttempt
class FilmAdmin(admin.ModelAdmin):
    list_display = ('tytul', 'reżyser', 'gatunek', 'rok_produkcji')
    search_fields = ('tytul', 'reżyser')

class SeansAdmin(admin.ModelAdmin):
    list_display = ('film', 'data_i_godzina')
    list_filter = ('data_i_godzina', 'film')

class RezerwacjaAdmin(admin.ModelAdmin):
    list_display = ('id', 'uzytkownik', 'seans', 'data_rezerwacji')
    list_filter = ('seans', 'uzytkownik')

@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'failures', 'is_locked')
    list_filter = ('is_locked',)
    search_fields = ('username',)
    list_editable = ('is_locked',)
    actions = ['reset_attempts_and_unlock']

    @admin.action(description='Zresetuj próby i odblokuj zaznaczone konta')
    def reset_attempts_and_unlock(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Pomyślnie zresetowano i odblokowano wybrane konta.")

admin.site.register(Film, FilmAdmin)
admin.site.register(Seans, SeansAdmin)
admin.site.register(Rezerwacja, RezerwacjaAdmin)

from .forms import AdminCaptchaForm
admin.site.login_form = AdminCaptchaForm