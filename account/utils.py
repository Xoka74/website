from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from six import text_type

User = get_user_model()


def send_confirmation_email(user_email, link):
    user = get_object_or_404(User, email=user_email)
    email = EmailMessage(
        f'Hi, {user.username}',
        f'To verify your account, follow this link: {link}',
        settings.EMAIL_HOST_USER,
        [user_email],
    )

    email.send(fail_silently=False)


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.pk) + text_type(timestamp)


token_generator = AppTokenGenerator()
