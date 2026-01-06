from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"Profil użytkownika: {self.user.username}"

class Film(models.Model):
    tytul = models.CharField(max_length=200)
    opis = models.TextField()
    rok_produkcji = models.IntegerField(default=2024)
    plakat = models.ImageField(upload_to='plakaty/', null=True, blank=True)
    reżyser = models.CharField(max_length=150, null=True, blank=True)
    gatunek = models.CharField(max_length=100, null=True, blank=True)
    kraj_pochodzenia = models.CharField(max_length=100, null=True, blank=True)
    zwiastun_url = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.tytul

    def srednia_ocena(self):
        recenzje = self.recenzje.all()
        if recenzje:
            return sum(r.ocena for r in recenzje) / len(recenzje)
        return 0

    def ilosc_gwiazdek(self):
        """Zwraca dokładną liczbę gwiazdek bez zaokrąglania (0-5)"""
        return self.srednia_ocena()

class Recenzja(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='recenzje')
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    ocena = models.FloatField(default=5.0, validators=[MinValueValidator(0.5), MaxValueValidator(5.0)])
    tresc = models.TextField(blank=True)
    data_dodania = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('film', 'uzytkownik')

    def __str__(self):
        return f"Recenzja {self.uzytkownik.username} dla {self.film.tytul}"

class Seans(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    data_i_godzina = models.DateTimeField()

    def __str__(self):
        return f"{self.film.tytul} - {self.data_i_godzina.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Seans"
        verbose_name_plural = "Seanse"

class Rezerwacja(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    seans = models.ForeignKey(Seans, on_delete=models.CASCADE)
    miejsca = models.TextField()
    data_rezerwacji = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rezerwacja nr {self.id} dla {self.uzytkownik.username} na {self.seans.film.tytul}"

    class Meta:
        verbose_name = "Rezerwacja"
        verbose_name_plural = "Rezerwacje"

class LoginAttempt(models.Model):
    username = models.CharField(max_length=150, db_index=True)
    failures = models.PositiveIntegerField(default=0)
    is_locked = models.BooleanField(default=False)
    lock_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Próby logowania dla: {self.username}"


@receiver(post_save, sender=User)
def create_user_profil(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profil(sender, instance, **kwargs):
    if hasattr(instance, 'profil'):
        instance.profil.save()