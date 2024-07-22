from django.urls import path

from .views import register, verify, profile, CustomPasswordResetView, login, logout, verification_email, email_sent, admin_panel, block_user, unblock_user, make_admin

app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('verify/<uidb64>/<token>/', verify, name='verify'),
    path('profile/', profile, name='profile'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('verification_email/', verification_email, name='verification_email'),
    path('email_sent/', email_sent, name='email_sent'),
    path('admin_panel/', admin_panel, name='admin_panel'),
    path('block_user/<int:user_id>/', block_user, name='block_user'),
    path('unblock_user/<int:user_id>/', unblock_user, name='unblock_user'),
    path('make_admin/<int:user_id>/', make_admin, name='make_admin'),
]