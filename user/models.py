from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import Group 
from .managers import UserManager
from django.utils.html import format_html
from django.template.defaultfilters import slugify
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone


class User(AbstractBaseUser):

    photo = models.ImageField('Profile photo', upload_to='user/user_photo', null=True, blank=True)
    email = models.EmailField(verbose_name='Email', unique=True, null=True, blank=True)
    username = models.CharField(max_length=85, unique=True)
    fullname = models.CharField(max_length=95)
    bio = models.CharField(max_length=120, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['fullname']

    def __str__(self):
        return self.username 
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin 

    def profile_photo(self):
        if self.photo:
            url = self.photo.url
        else:
            url = '/static/user/img/default_profile.jpg'
        return format_html(f'<img src="{url}" style="width: 3rem; margin: auto; "/>') 

    def get_absolute_url(self):
        return reverse("user-profile", kwargs={"username": self.username})


class Otp(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    rand_code = models.CharField( max_length=4)

    def __str__(self):
        return f'{self.user} - {self.rand_code}'

    def timer(self):
        return self.created >= timezone.now() - timedelta(minutes=1)
    
    def end_time(self):
        return self.created + timedelta(minutes=10)