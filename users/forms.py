from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ('email', 'nickname', 'password1', 'password2')

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254)

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)