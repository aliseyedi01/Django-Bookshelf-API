import uuid
import secrets
# django
from django.db import models
from django.contrib.auth.hashers import check_password

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ["email", "username"]

    @property
    def is_anonymous(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def check_password(self, password):
        return check_password(password, self.password)

class OtpToken(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    otp_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    expires_at = models.DateTimeField(blank=True, null=True, editable=False)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Generate a unique OTP code
        while True:
            unique_otp_code = secrets.token_hex(3)
            if not OtpToken.objects.filter(otp_code=unique_otp_code).exists():
                self.otp_code = unique_otp_code
                break
        super().save(*args, **kwargs)