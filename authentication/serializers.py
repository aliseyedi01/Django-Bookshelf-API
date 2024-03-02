# django
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# drf
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
# apps
from .models import User
import re


MAX_NAME_LENGTH = 30

class UserSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=MAX_NAME_LENGTH, required=True)
    last_name = serializers.CharField(max_length=MAX_NAME_LENGTH, required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'created_at')
        read_only_fields = ('id', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value

    def validate_password(self, value):
        MIN_LENGTH = 6
        password_regex = r"(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)"  # Regex for password complexity

        if len(value) < MIN_LENGTH:
            raise serializers.ValidationError(f"Password must be at least {MIN_LENGTH} characters long")

        # Optional check for common password patterns (consider using a third-party library for a more comprehensive list)
        common_passwords = ["password", "123456", "qwerty"]
        if value.lower() in common_passwords:
            raise serializers.ValidationError("Please choose a stronger password. This password is commonly used and vulnerable to attacks.")

        if not re.search(password_regex, value):
            raise serializers.ValidationError(
                "Password must include at least one uppercase letter, lowercase letter, number, and symbol"
            )

        return value

    def validate_first_name(self, value):
        if len(value) > MAX_NAME_LENGTH:
            raise serializers.ValidationError(f"First name cannot exceed {MAX_NAME_LENGTH} characters.")
        return value

    def validate_last_name(self, value):
        if len(value) > MAX_NAME_LENGTH:
            raise serializers.ValidationError(f"Last name cannot exceed {MAX_NAME_LENGTH} characters.")
        return value




class SingInSerializer(serializers.ModelSerializer):
    username_or_email = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username_or_email', 'password')
        read_only_fields = ('id', 'created_at')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        username_or_email = data.get("username_or_email")
        password = data.get("password")

        # Check if username or email is provided
        if not username_or_email:
            raise serializers.ValidationError("Username or email is required.")

        # Attempt to authenticate using both username and email
        user = User.objects.filter(
            Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)
        ).first()

        if user is None:
            raise serializers.ValidationError("Invalid credentials555.")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid password.")

        # if user is None or not user.check_password(password):
        #     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return data




class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(f'User with this {value} does not exist')
        return value