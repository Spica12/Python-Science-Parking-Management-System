import six

from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .models import UserRole


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        user_role = UserRole.objects.get(user=user)
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user_role.is_verified)
        )

account_activation_token = AccountActivationTokenGenerator()