from django.urls import path

from .views import register, verify, profile, CustomPasswordResetView, login, logout, verification_email, email_sent, verify_user

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
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
    path('verify_user/<int:user_id>/', verify_user, name='verify_user'),
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
    # FOR TESTING DELETE ON RELEASE
]