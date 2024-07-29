from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.urls import reverse_lazy
from django.db.models import Q

from finance.models import Account


from .forms import CustomPasswordResetForm, CustomUserCreationForm, LoginForm, ManageProfileForm, CustomPasswordChangeForm
from .models import CustomUser, UserRole
from .tokens import account_activation_token
from .utils import send_activation_email
from .decorators import user_is_active, user_is_verified

    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
@login_required
def verify_user(request, user_id):
    user_role = get_object_or_404(UserRole, user_id=user_id)
    user_role.is_verified = True
    user_role.save()
    return redirect('users:profile')
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE


def get_user_role(user):
    return get_object_or_404(UserRole, user=user)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            account = Account(user=user)
            account.save()

            is_first_user = CustomUser.objects.count() == 1

            if is_first_user:
                UserRole.objects.create(user=user, is_admin=True, is_verified=True)
            else:
                UserRole.objects.create(user=user)

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
                user_role = UserRole.objects.get(user=user)
                if not user_role.is_active:
                    form.add_error(None, 'Your account has been blocked. Please contact support.')
                else:
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

@login_required
def manage_profile(request):
    if request.method == 'POST':
        form = ManageProfileForm(request.POST, instance=request.user, request=request)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ManageProfileForm(instance=request.user, request=request)

    return render(request, 'users/manage_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('users:profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
