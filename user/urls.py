from django.urls import path
from .views import UserLogoutView, UserSigninView, UserSignupView, UserProfileView, UserUpdateView, create_otp_view, check_otp_view, PasswordUpdateView

urlpatterns = [
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('signin/', UserSigninView.as_view(), name='user-signin'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('profile/changepass', PasswordUpdateView.as_view(), name='user-password'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/<str:username>/edit/', UserUpdateView.as_view(), name='user-edit'),
    path('create/otp', create_otp_view, name='create-otp'),
    path('check/otp', check_otp_view, name='check-otp'),
]
