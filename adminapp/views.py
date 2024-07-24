from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from users.models import CustomUser
from .decorators import admin_required, admin_or_operator_required

@admin_required
def admin_panel(request):
    query = request.GET.get('query', '')
    users = CustomUser.objects.all()

    if query:
        users = users.filter(
            Q(email__icontains=query) |
            Q(nickname__icontains=query) |
            Q(id__icontains=query)
        )

    return render(request, 'adminapp/admin_panel.html', {'users': users, 'query': query})

@admin_required
def block_user(request, user_id):
    user_to_block = get_object_or_404(CustomUser, id=user_id)
    current_user = request.user

    if user_to_block.userrole.is_admin:
        messages.error(request, "You cannot block another admin.")
    else:
        user_to_block.userrole.is_active = False
        user_to_block.userrole.save()
        messages.success(request, f"User {user_to_block.email} has been blocked.")
    
    return redirect('adminapp:admin_panel')

@admin_required
def unblock_user(request, user_id):
    user_to_unblock = get_object_or_404(CustomUser, id=user_id)
    user_to_unblock.userrole.is_active = True
    user_to_unblock.userrole.save()
    messages.success(request, f"User {user_to_unblock.email} has been unblocked.")
    return redirect('adminapp:admin_panel')

@admin_required
def make_admin(request, user_id):
    user_to_promote = get_object_or_404(CustomUser, id=user_id)
    if user_to_promote.userrole.is_admin:
        messages.info(request, "User is already an admin.")
    else:
        user_to_promote.userrole.is_admin = True
        user_to_promote.userrole.is_verified = True
        user_to_promote.userrole.save()
        messages.success(request, f"User {user_to_promote.email} has been promoted to admin.")
    return redirect('adminapp:admin_panel')

@admin_required
def make_operator(request, user_id):
    user_to_promote = get_object_or_404(CustomUser, id=user_id)
    if user_to_promote.userrole.is_operator:
        messages.info(request, "User is already an operator.")
    else:
        user_to_promote.userrole.is_operator = True
        user_to_promote.userrole.save()
        messages.success(request, f"User {user_to_promote.email} has been promoted to operator.")
    return redirect('adminapp:admin_panel')