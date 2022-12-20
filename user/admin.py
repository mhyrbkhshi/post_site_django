from django.contrib import admin
from .models import User, Otp
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import forms
from client_side_image_cropping import DcsicAdminMixin

class UserAdmin(BaseUserAdmin, DcsicAdminMixin):
    form = forms.ChangeUserForm
    add_form = forms.CreationUserForm

    fieldsets = (
    ('Main info', {'fields': ('photo','email', 'password', 'username', 'group', 'bio', 'fullname')}),
    ('Permissions', {'fields': ('is_admin','is_active')}),) 

    add_fieldsets = (None, {
    'classes': ('wide',),
    'fields': ('photo', 'username', 'fullname', 'group', 'password1', 'password2'),}),

    list_display = ['username', 'email', 'is_admin','is_active', "group", "profile_photo"]
    list_filter = ['is_admin', 'is_active']
    search_fields = ['email', 'username']
    search_help_text = 'Enter email or username for searching'
    ordering = ['email']
    filter_horizontal = ()

class OtpAdmin(admin.ModelAdmin):
    model = Otp
    list_display = ['user', 'email', 'rand_code', 'timer']

admin.site.register(User, UserAdmin)
admin.site.register(Otp, OtpAdmin)