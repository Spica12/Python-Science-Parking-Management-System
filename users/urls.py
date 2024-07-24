from django.urls import path

from .views import (register, verify, profile, login, logout, verification_email, email_sent, 
                    manage_profile, change_password, CustomPasswordResetView, 
                    CustomPasswordResetDoneView, CustomPasswordResetConfirmView, 
                    CustomPasswordResetCompleteView, verify_user)
app_name = 'users'

urlpatterns = [
    path('register/', register, name='register'),
    path('verify/<uidb64>/<token>/', verify, name='verify'),
    path('profile/', profile, name='profile'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('verification_email/', verification_email, name='verification_email'),
    path('email_sent/', email_sent, name='email_sent'),
    path('manage_profile/', manage_profile, name='manage_profile'),
    path('change_password/', change_password, name='change_password'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
    path('verify_user/<int:user_id>/', verify_user, name='verify_user'),
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
]