import hashlib
import secrets
from django.db import models


class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """Hash the raw password with SHA-256 and store it."""
        self.password_hash = hashlib.sha256(raw_password.encode('utf-8')).hexdigest()

    def check_password(self, raw_password):
        """Verify a raw password against the stored SHA-256 hash."""
        return self.password_hash == hashlib.sha256(raw_password.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.username


class AuthToken(models.Model):
    key = models.CharField(max_length=64, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tokens')
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate(cls, user):
        """Create a new token for the given user, removing old ones."""
        cls.objects.filter(user=user).delete()
        token = cls.objects.create(
            key=secrets.token_hex(32),
            user=user,
        )
        return token

    def __str__(self):
        return f"Token for {self.user.username}"
