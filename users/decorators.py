from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserRole

def is_active(user):
    user_role = get_object_or_404(UserRole, user=user)
    return user_role.is_active

def is_verified(user):
    user_role = get_object_or_404(UserRole, user=user)
    return user_role.is_verified

def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.userrole.is_admin)(view_func))
    return decorated_view_func

def admin_or_operator_required(view_func):
    def check_role(user):
        user_role = get_object_or_404(UserRole, user=user)
        return user_role.is_admin or user_role.role == 'operator'

    decorated_view_func = login_required(user_passes_test(check_role)(view_func))
    return decorated_view_func

def user_is_active(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not is_active(request.user):
            return HttpResponseForbidden("Your account is inactive. Please contact support.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_is_verified(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not is_verified(request.user):
            return HttpResponseForbidden("Your account is not verified. Please verify your account.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view