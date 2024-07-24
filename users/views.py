from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import PasswordResetView
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import CustomPasswordResetForm, CustomUserCreationForm, LoginForm
from .models import CustomUser, UserRole
from .tokens import account_activation_token
from .utils import send_activation_email
from .decorators import user_is_active, user_is_verified

def get_user_role(user):
    return get_object_or_404(UserRole, user=user)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            UserRole.objects.create(user=user, role='Customer', is_verified=False)
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def verification_email(request):
    user = request.user
    
    if not user.email:
        messages.error(request, 'Email address not set.')
        return redirect('users:profile')
    
    user_role = get_user_role(user)
    
    if user_role.is_verified:
        messages.info(request, 'Your account is already verified.')
        return redirect('users:profile')
    
    send_activation_email(user, request)
    messages.success(request, 'Verification email has been sent.')
    return redirect('users:email_sent')

def verify(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        user_role = get_user_role(user)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
        user_role = None

    if user is not None and account_activation_token.check_token(user, token):
        if not user_role.is_verified:
            user_role.is_verified = True
            user_role.save()
            messages.success(request, 'Your account has been verified.')
        else:
            messages.info(request, 'Your account is already verified.')
    else:
        messages.error(request, 'Verification link is invalid or expired.')

    return redirect('users:profile')

@login_required
@user_is_active
def profile(request):
    user = request.user
    user_role = get_user_role(user)
    
    if not user_role.is_active:
        return HttpResponseForbidden("Your account is inactive. Please contact support.")
    
    return render(request, 'users/profile.html', {'user': user, 'user_role': user_role})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                auth_login(request, user)
                return redirect('users:profile')
            else:
                form.add_error(None, 'Invalid email or password')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('users:login')

def email_sent(request):
    return render(request, 'users/email_sent.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')
    form_class = CustomPasswordResetForm