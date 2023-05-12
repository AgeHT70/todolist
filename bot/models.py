import secrets

from django.db import models

from core.models import User


class TgUser(models.Model):
    """TgUser model with necessary attributes"""

    chat_id = models.BigIntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    verification_code = models.CharField(max_length=100, null=True, blank=True, default=None)

    @staticmethod
    def generate_verification_code() -> str:
        return str(secrets.token_urlsafe(32))
