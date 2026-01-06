from django.core.management.base import BaseCommand
from main.models import LoginAttempt

class Command(BaseCommand):
    help = 'Resetuje wszystkie blokady kont użytkowników.'

    def handle(self, *args, **options):
        LoginAttempt.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Pomyślnie zresetowano wszystkie blokady logowania.'))