import uuid
import secrets
# django
from django.db import models
from django.contrib.auth.hashers import check_password

class User(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def check_password(self, password):
        return check_password(password, self.password)

class OtpToken(models.Model):
    uuid = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    expires_at = models.DateTimeField(blank=True, null=True,editable=False)

    def __str__(self):
        return self.user.username