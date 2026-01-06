from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class EmailOrUsernameBackend(BaseBackend):
    """
    Ten backend pozwala użytkownikom logować się za pomocą
    nazwy użytkownika lub adresu email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=username).first()
        user = user_by_username or user_by_email
        if user and user.check_password(password):
            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None