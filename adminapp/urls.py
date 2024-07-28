from django.urls import path
from .views import admin_panel, block_user, unblock_user, change_role, user_management, change_user_status, vehicles_management, change_vehicle_status, user_management_operator

app_name = 'adminapp'

urlpatterns = [
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('change_role/<int:user_id>/', change_role, name='change_role'),
    path('change-user-status/<int:user_id>/', change_user_status, name='change_user_status'),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock_user'),
    path('user_management/', user_management, name='user_management'),
    path('user_management_operator', user_management_operator, name='user_management_operator'),
    path('vehicles_management/', vehicles_management, name='vehicles_management'),
    path('vehicles/<int:vehicle_id>/change_status/', change_vehicle_status, name='change_vehicle_status'),
]