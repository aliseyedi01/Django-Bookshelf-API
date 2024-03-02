from django.db import models
import uuid
import secrets


class User(models.Model):
    uuid = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class OtpToken(models.Model):
    uuid = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    expires_at = models.DateTimeField(blank=True, null=True,editable=False)

    def __str__(self):
        return self.user.username