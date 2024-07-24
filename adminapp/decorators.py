from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import UserRole

def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.userrole.is_admin)(view_func))
    return decorated_view_func

def admin_or_operator_required(view_func):
    def check_role(user):
        user_role = get_object_or_404(UserRole, user=user)
        return user_role.is_admin or user_role.role == 'operator'

    decorated_view_func = login_required(user_passes_test(check_role)(view_func))
    return decorated_view_func