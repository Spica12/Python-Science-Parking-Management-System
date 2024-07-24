from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.core.mail import EmailMultiAlternatives

def send_activation_email(user, request):
    try:
        current_site = request.get_host()
        mail_subject = 'Activate your account'
        html_message = render_to_string('activation_email.html', {
            'user': user,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        plain_message = strip_tags(html_message)
        email = EmailMultiAlternatives(
            mail_subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
    
def send_password_reset_email(user_email, reset_link):
    subject = 'Password Reset Request'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = user_email

    html_content = render_to_string('users/password_reset_email.html', {
        'reset_link': reset_link,
        'protocol': 'http',
        'domain': '127.0.0.1:8000',
        'current_year': 2024
    })
    
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    email.attach_alternative(html_content, "text/html")
    email.send()