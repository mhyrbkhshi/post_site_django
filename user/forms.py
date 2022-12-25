from django import forms 
from .models import User , Otp
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError 
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from client_side_image_cropping import ClientsideCroppingWidget
from random import randint


class CreationUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', max_length=120, widget=forms.PasswordInput())
    password2 = forms.CharField(label='Confirm password', max_length=120, widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['photo', 'username', 'group', 'bio']
        widgets = {
            'photo': ClientsideCroppingWidget(
                width=900, height=900,preview_width=50,preview_height=50
            )
        }
        
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password1 != password2:
            raise ValidationError('Passwords doesn\'t match','passwords not match')
        
        return password2

    def save(self, commit: bool =True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user 

class ChangeUserForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User 
        fields = ['photo','email', 'password', 'username', 'group', 'is_active', 'is_admin', 'bio']
        widgets={
            'photo': ClientsideCroppingWidget(
                width=900, height=900,preview_width=150,preview_height=150
            )
        }



class UserLoginForm(forms.Form):
    email_username = forms.CharField(label='Email or username' ,widget=forms.TextInput(attrs={
        'placeholder':'Email address or username',
        'class':'form-control',
    }))
    password = forms.CharField(label='Password', max_length=120, widget=forms.PasswordInput(attrs={
        'placeholder':'Password',
        'class':'form-control',
    }))

    def clean_email_username(self):
        email_username = self.cleaned_data['email_username']

        if User.objects.filter(email=email_username):
            return email_username

        elif User.objects.filter(username=email_username):
            return email_username

        else:
            raise ValidationError('This email or username dos\'t exsit')

class ClientUserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Password',
    }))

    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm password',
    }))
    class Meta:
        model = User 
        fields = ['photo', 'username', 'fullname', 'bio']
        widgets = {
            'photo': ClientsideCroppingWidget(width=900, height=900, preview_width='none', preview_height='none',),
            'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
            'fullname':forms.TextInput(attrs={'class':'form-control','placeholder':'Fullname'}),
            'bio':forms.TextInput(attrs={'class':'form-control','placeholder':'Bio'}),
            }
    
    def save(self, commit=True):
        client_group = Group.objects.filter(name='client')

        if client_group:
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            user.group = client_group.last()

            if commit:
                user.save()

            return user
        else: 

            raise ValueError('Please make a group and named it "client" and give permissions you want to it. (this message is for admin user)')

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password1 != password2:
            raise ValidationError('Passwords doesn\'t match')
        else :
            return password2

class ClientUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['photo', 'username', 'fullname', 'bio']
        widgets = {
            'photo': ClientsideCroppingWidget(
                width=900, height=900, preview_width='none', preview_height='none',),
            'username':forms.TextInput(attrs={
                'class':"form-control"
            }),
            'fullname':forms.TextInput(attrs={
                'class':"form-control"
            }),
            'bio':forms.Textarea(attrs={
                'id':'area_input',
                'class':"form-control"
            })
        }


class CreateOtpForm(forms.Form):
    email = forms.EmailField(max_length=220, required=True, widget=forms.EmailInput(attrs={
        'class':'form-control',
    }))

    def clean_email(self):
        email = self.cleaned_data['email']

        if not User.objects.filter(email=email):
            return email
        else:
            raise ValidationError('this email address exist')

    def save(self, user):
        code = randint(1000, 9999)
        print(code)
        return Otp.objects.create(rand_code=code, user=user, email=self.cleaned_data['email'])


class CheckOtpForm(forms.Form):
    rand_code = forms.CharField(label='Code', max_length=4, widget=forms.TextInput(attrs={
        'class':'form-control',
    }))

    def check_rand_code(self, rand_code):
        if rand_code == self.cleaned_data['rand_code']:
            return True 
        else:
            return False

class ChangePasswordForm(forms.Form):
    old_pass = forms.CharField(label='Your last password', max_length=120, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Your last password',
    }))

    password = forms.CharField(label='New password', max_length=120, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'New password',
    }))

    pass_confirm = forms.CharField(label='Confirm new password', max_length=120, widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Confirm new password',
    }))

    def clean_pass_confirm(self):
        password = self.cleaned_data.get('password')
        pass_confirm = self.cleaned_data['pass_confirm']

        if password and pass_confirm != password:
            raise ValidationError('Password does not match with confirm password', 'not-same-pass')

        return pass_confirm