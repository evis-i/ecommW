import copy
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegistrationForm, UserEditForm
from .tokens import account_activation_token
from .models import UserBase
from basket.basket import Basket
from django.conf import settings


# Create your views here.
@login_required
def dashboard(request):
    #orders = user_orders(request)
    return render(request,
                  'account/dashboard.html',)
                #  {'section': 'profile', 'orders': orders})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
            print("ok")
        else:
            print(user_form.is_valid())

    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'account/edit_profile.html', {'user_form':user_form})

@login_required
def deactivate_user(request):
    user = UserBase.objects.get(user_name=request.user)
    user.is_active=False
    user.save()
    logout(request)
    return redirect('account:deactivate_confirmation')

def logoutUser(request):
    basket = copy.deepcopy(Basket(request).basket)
    logout(request)
    session = request.session
    session[settings.BASKET_SESSION_ID] = basket
    session.modified = True
    return redirect('account:login')

def account_register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()
            # Setup email
            current_site = get_current_site(request)
            subject = 'Activate your account'
            message = render_to_string('account/reg_acc_act_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('Registered successfully and activation sent')
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/register.html', {'form': registerForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/activation_invalid.html')