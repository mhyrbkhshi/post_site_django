from django.shortcuts import render,redirect,get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout
from django.views.generic import View, ListView, UpdateView
from django.contrib.auth import authenticate
from .forms import UserLoginForm, ClientUserCreateForm, ClientUserEditForm, CreateOtpForm, CheckOtpForm,ChangePasswordForm
from .models import User, Otp
from django.http import Http404


class UserLogoutView(View):
    def get(self, request): 
        if request.user.is_authenticated:
            return render(request, 'user/user_logout.html',{'form_name':'Logout'})
        else:
            raise ValueError('Anonymose user can not logout')

    def post(selfm, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect(reverse('home-index'))
        else:
            raise ValueError('Anonymose user can not logout')


def get_form_response(request, template_name, form_name, form=None):

        return render(request, template_name,{
            'form_name':form_name,
            'form':form,
        })


class UserSigninView(View):
    form = UserLoginForm
    template_name = 'user/user_signin.html'

    def get(self, request):
        return get_form_response(request, self.template_name, 'Signin', self.form())

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            
            user = authenticate(request, username=form.cleaned_data['email_username'], password=form.cleaned_data['password'])
            if not user :
                form.add_error('password', 'Password does\'t match')
                return get_form_response(request, self.template_name, 'Signin', form)

            else:
                login(request, user)
                return redirect(reverse('user-profile', args=[user.username]))
        else:
            return get_form_response(request, self.template_name, 'Signin', form)



class UserSignupView(View):
    template_name = 'user/user_signup.html'
    form = ClientUserCreateForm

    def get(self, request):
        if not request.user.is_authenticated:
            return get_form_response(request, self.template_name, 'Signup', self.form())
        else:
            raise ValueError('You are in account you can\'t create another')
    
    def post(self, request):
        if not request.user.is_authenticated:
            form = self.form(request.POST)

            if form.is_valid():
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse('create-otp'))
            else:
                return get_form_response(request, self.template_name, 'signup', form)

        else:
            raise ValueError('You are in account you can\'t create another')


class UserProfileView(ListView):
    paginate_by = 6
    template_name = 'user/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_target"] = get_object_or_404(User, username=self.kwargs['username'])
        return context
    

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.post_set.all()


class UserEditView(UpdateView):
    form_class=ClientUserEditForm
    model=User 
    template_name = 'user/user_update.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = 'edit profile'
        return context
    
    def get(self, request, *args, **kwargs):

        target_user = self.get_object()
        if target_user == request.user:
            return super().get(request, *args, **kwargs)
        
        raise Http404()

    def post(self, request, *args, **kwargs):
        target_user = self.get_object()
        if target_user == request.user:
            return super().post(request, *args, **kwargs)
        
        raise Http404()

def create_otp_view(request):
    user = request.user
    otp = user.otp_set.last()

    if user.is_authenticated:
        if otp:
            if otp.timer():
                return redirect(reverse('check-otp'))

            else:
                otp.delete()

        if request.method == 'GET':
            return render(request, 'user/otp_form.html', {'form':CreateOtpForm(), 'form_name':'Confirm email'})

        elif request.method == 'POST':
            form = CreateOtpForm(request.POST)
            if form.is_valid():
                form.save(user)
                return HttpResponseRedirect(reverse('check-otp'))

            else:
                return render(request, 'user/otp_form.html', {'form':form, 'form_name':'confirm email'})
        
    else:
        raise Http404()

def check_otp_view(request):
    user = request.user
    otp = user.otp_set.last()
    
    if user.is_authenticated:
        if not otp:
            return redirect(reverse('create-otp'))
            
        else:
            if otp.timer():
                if request.method == 'GET':
                    return render(request, 'user/otp_check.html', {'form':CheckOtpForm(),'form_name':'check code','otp':otp})

                elif request.method == 'POST':
                    form  = CheckOtpForm(request.POST)

                    if form.is_valid():
                        if form.check_rand_code(otp.rand_code):
                            user.email = otp.email
                            user.save()
                            otp.delete()
                            return HttpResponseRedirect(user.get_absolute_url())
                        else:
                            form.add_error('rand_code', 'Code does not match')
                    
                    return render(request, 'user/otp_check.html', {'form':form,'form_name':'Confirm email','otp':otp})

            else :
                otp.delete()
                return redirect(reverse('create-otp'))

    else: 
        raise Http404()

class UpdatePassView(View):
    form_class = ChangePasswordForm
    template_name = 'user/password_form.html'

    def get(self, request):
        if request.user.is_authenticated :
            return get_form_response(request, self.template_name,'Change password', self.form_class())
        else : raise Http404()

    def post(self, request):
        if request.user.is_authenticated :
            form = self.form_class(request.POST)
            if form.is_valid():
                old_pass = form.cleaned_data['old_pass']
                if request.user.check_password(old_pass):
                    request.user.set_password(form.cleaned_data['password'])
                    return HttpResponseRedirect(reverse('home-index'))

                else:
                    form.add_error('old_pass', 'This password does not match')

            return get_form_response(request, self.template_name, 'Change password', form)  

        else : raise Http404