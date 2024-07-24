from django.urls import path
from .views import admin_panel, block_user, unblock_user, change_role, user_management

app_name = 'adminapp'

urlpatterns = [
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('change_role/<int:user_id>/', change_role, name='change_role'),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock_user'),
    path('user_management/', user_management, name='user_management'),
]