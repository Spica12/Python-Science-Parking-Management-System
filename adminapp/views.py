from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from users.models import CustomUser, UserRole
from vehicles.models import Vehicle
from adminapp.decorators import admin_required, admin_or_operator_required
from users.decorators import user_is_active

@user_is_active
@admin_or_operator_required
def admin_panel(request):
    return render(request, 'adminapp/admin_panel.html')

@admin_required
def user_management(request):
    user_id = request.GET.get('user_id')
    query = request.GET.get('query', '')

    if user_id:
        users = CustomUser.objects.filter(id=user_id)
    elif query:
        users = CustomUser.objects.filter(
            Q(email__icontains=query) | Q(nickname__icontains=query) | Q(id__icontains=query)
        )
    else:
        users = CustomUser.objects.all()
    
    return render(request, 'adminapp/user_management.html', {'users': users, 'query': query, 'user_id': user_id})

@admin_or_operator_required
def vehicles_management(request):
    user_id = request.GET.get('user_id')
    query = request.GET.get('query', '')

    if user_id:
        vehicles = Vehicle.objects.filter(user_id=user_id)
    else:
        if query:
            vehicles = Vehicle.objects.filter(
                Q(user__id__icontains=query) | Q(plate_number__icontains=query)
            )
        else:
            vehicles = Vehicle.objects.all()

    paginator = Paginator(vehicles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'adminapp/vehicles_management.html', {'page_obj': page_obj, 'query': query})

@require_POST
@admin_required
def change_vehicle_status(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    action = request.POST.get('action')

    if action == 'block':
        vehicle.status = 'BLOCKED'
    elif action == 'unblock':
        vehicle.status = 'ACTIVE'
    elif action == 'delete':
        vehicle.delete()
        messages.success(request, f"Vehicle {vehicle.plate_number} has been deleted.")
        return redirect('adminapp:vehicles_management')

    vehicle.save()
    messages.success(request, f"Vehicle {vehicle.plate_number} status has been updated.")
    return redirect('adminapp:vehicles_management')

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
    
    return redirect('adminapp:user_management')

@admin_required
def unblock_user(request, user_id):
    user_to_unblock = get_object_or_404(CustomUser, id=user_id)
    user_to_unblock.userrole.is_active = True
    user_to_unblock.userrole.save()
    messages.success(request, f"User {user_to_unblock.email} has been unblocked.")
    return redirect('adminapp:user_management')

@require_POST
@admin_required
def change_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    new_role = request.POST.get('role')

    if new_role:
        user_role = user.userrole
        if new_role == 'Admin':
            user_role.is_admin = True
            user_role.is_operator = False
        elif new_role == 'Operator':
            user_role.is_operator = True
            user_role.is_admin = False
        else:
            user_role.is_admin = False
            user_role.is_operator = False

        user_role.role = new_role
        user_role.save()

    return redirect('adminapp:user_management')

@admin_required
def change_user_status(request, user_id):
    user_role = get_object_or_404(UserRole, user_id=user_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'verify':
            user_role.is_verified = True
        elif action == 'unverify':
            user_role.is_verified = False
        elif action == 'block':
            user_role.is_active = False
        elif action == 'unblock':
            user_role.is_active = True
        
        user_role.save()
    
    return redirect('adminapp:user_management')
