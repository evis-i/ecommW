from django.contrib.auth import views as dj_auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views
from .forms import UserLoginForm, PwdResetForm, PwdResetConfirmForm

app_name = 'account'

urlpatterns = [
    path('register/', views.account_register, name='register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', dj_auth_views.LoginView.as_view(template_name='account/login.html',
                                                   form_class=UserLoginForm), name='login'),
    path('logout/', views.logoutUser, name='logout'),
   # path('logout/', dj_auth_views.LogoutView.as_view(next_page='/account/login/'), name='logout'),
    path('profile/edit/', views.edit_profile, name='editProfile'),
    path('profile/deactivate_user/', views.deactivate_user, name='deactivate_user'),
    path('profile/deactivate_confirm/', TemplateView.as_view(template_name="account/deactivate_confirm.html"),
         name='deactivate_confirmation'),
    path('password_reset/', dj_auth_views.PasswordResetView.as_view(template_name="account/password_reset.html",
                                                                   success_url="password_reset_email_confirm",
                                                                   email_template_name="account/password_reset_email.html",
                                                                   form_class=PwdResetForm),
         name='pwdreset'),
    path('password_reset/password_reset_email_confirm', TemplateView.as_view(template_name="account/reset_status.html"),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', dj_auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html',
                                                                                                success_url='/account/password_reset_complete/',
                                                                                                form_class=PwdResetConfirmForm),
         name="password_reset_confirm"),
    path('password_reset_complete/', TemplateView.as_view(template_name="account/reset_status.html"),
         name='password_reset_complete'),

]
