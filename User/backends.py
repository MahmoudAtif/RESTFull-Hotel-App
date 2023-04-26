from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class CustomBackends(ModelBackend):
    def authenticate(username, password, **kwargs):
        User = get_user_model()
        
        try:
            user = User.objects.get(
                Q(username=username) |
                Q(email=username))
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


