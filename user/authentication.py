from django.contrib.auth.backends import BaseBackend
from user.models import User

class EmailAuthenticate(BaseBackend):
    def authenticate(self, request, username=None, password=None):

        try:
            user = User.objects.get(email=username)

        except User.DoesNotExist:
            return None
        
        else:
            if user.check_password(password):
                return user
                
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)

        except User.DoesNotExist:
            return None