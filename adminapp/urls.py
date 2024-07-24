from django.urls import path
from .views import admin_panel, block_user, unblock_user, make_admin

app_name = 'adminapp'

urlpatterns = [
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock_user'),
    path('make_admin/<int:user_id>/', make_admin, name='make_admin'),
]
