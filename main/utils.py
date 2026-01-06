from django.contrib.auth import get_user_model

def is_admin_by_username(username):
    User = get_user_model()
    if not username:
        return False
    try:
        user = User.objects.get(username=username)
        if user.is_superuser or user.is_staff:
            return True
    except User.DoesNotExist:
        pass
    return False