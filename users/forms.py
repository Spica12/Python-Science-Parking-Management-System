from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse_lazy

from .models import CustomUser
from .utils import send_activation_email
from .tokens import account_activation_token
from .utils import send_password_reset_email

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        if commit:
            user.save()
        return user 
class CustomPasswordResetForm(PasswordResetForm):
    def get_users(self, email):
        active_users = CustomUser.objects.filter(
            email__iexact=email,
            userrole__is_active=True
        )
        return (user for user in active_users)
    
    def save(self, domain_override=None,
             subject_template_name='users/password_reset_subject.txt',
             email_template_name='users/password_reset_email.html',
             use_https=False, token_generator=account_activation_token,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generates a one-use only link for resetting password and sends to the user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            reset_link = request.build_absolute_uri(
                reverse_lazy('users:password_reset_confirm', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token_generator.make_token(user),
                })
            )
            send_password_reset_email(user.email, reset_link)
    
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class ManageProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = ['email', 'nickname']

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.email != self.initial['email']:
            user.userrole.is_verified = False
            user.userrole.save()
            if self.request:
                send_activation_email(user, self.request)
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Current Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password')

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password1', 'new_password2')