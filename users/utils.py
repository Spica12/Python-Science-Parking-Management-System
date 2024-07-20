from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token

def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = request.build_absolute_uri(reverse('users:verify', kwargs={'uidb64': uid, 'token': token}))

    email_subject = 'Verify your account'
    email_body = f"Hi {user.nickname},\nPlease click the link below to verify your account:\n{activation_link}"

    email = EmailMessage(email_subject, email_body, to=[user.email])
    email.send()