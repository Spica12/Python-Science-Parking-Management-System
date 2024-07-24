from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import UserRole

def is_active(user):
    user_role = get_object_or_404(UserRole, user=user)
    return user_role.is_active

def is_verified(user):
    user_role = get_object_or_404(UserRole, user=user)
    return user_role.is_verified

def user_is_active(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not is_active(request.user):
            return HttpResponseForbidden("Your account is blocked. Please contact support.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_is_verified(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not is_verified(request.user):
            return HttpResponseForbidden("Your account is not verified. Please verify your account.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view