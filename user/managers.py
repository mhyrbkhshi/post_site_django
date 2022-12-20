from django.contrib.auth.models import BaseUserManager 

class UserManager(BaseUserManager):
    def create_user(self, username, fullname, email=None, password=None):

        if not username:
            raise ValueError('Users must have an username')
        
        if email :
            email = self.normalize_email(email)

        user = self.model(
            email = email,
            username = username,
            fullname=fullname,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, fullname, email=None, password=None) :

        user = self.create_user(username, fullname, email, password)
        user.is_admin = True 
        user.save(using=self._db)
        return user