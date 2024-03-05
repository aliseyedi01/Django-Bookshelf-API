# django
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.messages import success, warning
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# apps
from .serializers import SingUpSerializer , ResendOtpSerializer , SingInSerializer , VerifyEmailSerializer
from .models import User , OtpToken
from .tokens import get_tokens_for_user
from .utils import generate_and_send_otp
# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class SignUpView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=SingUpSerializer,
        responses={
            201: "Account created successfully!",
            400: "Bad request (e.g., invalid data, missing required fields)",
        }
    )
    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user_data['password'] = make_password(serializer.validated_data['password'])

            username = user_data['username']
            cache_key = f'signup_data_{username}'

            cache.delete(cache_key)
            cache.set(cache_key, user_data, timeout=900)

            OtpToken.objects.filter(username=username).delete()
            otp = generate_and_send_otp(user_data)
            return Response({
                'Message': 'Account created successfully! An OTP has been sent to your email for verification',
                'data': { 'otp_test' :  otp.otp_code}
                },status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyEmailView(APIView):
    @swagger_auto_schema(
        request_body=VerifyEmailSerializer,
        responses={
            200: "Account activated successfully!",
            400: "Bad request (e.g., invalid OTP code, expired OTP)",
            404: "User with the provided username not found",
            401: "Unauthorized (if username or OTP is invalid)",
        }
    )
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            otp_code = serializer.validated_data['otp_code']

            cache_key = f'signup_data_{username}'

            cached_data = cache.get(cache_key)
            if not cached_data:
                return Response({'error': 'Cached data not found'}, status=status.HTTP_400_BAD_REQUEST)
            user = cached_data

            user_otp = OtpToken.objects.filter(username=username).order_by("created_at").first()
            if not user_otp:
                return Response({'error': 'No OTP found for this user'}, status=status.HTTP_400_BAD_REQUEST)

            if otp_code != user_otp.otp_code:
                return Response({'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)

            if user_otp.expires_at < timezone.now():
                return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)

            user_register = User.objects.create(**user)
            user_register.is_verified = True
            user_register.save()
            user_otp.delete()
            cache.delete(cache_key)

            return Response({
                'message': 'Your account has been activated successfully!'
                }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOtpView(APIView):
    @swagger_auto_schema(
        request_body=ResendOtpSerializer,
        responses={
            200: "A new OTP has been sent to your email address.",
            400: "Bad request (e.g., invalid data, missing required fields)",
            404: "User with the provided email not found",
            500: "Internal server error (e.g., email sending failure)",
        }
    )
    def post(self, request):
        serializer = ResendOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = request.data["username"]
        cache_key = f'signup_data_{username}'
        cached_data = cache.get(cache_key)
        if not cached_data:
            return Response({
                'error': 'Cached data not found'
                }, status=status.HTTP_400_BAD_REQUEST)

        try:
            OtpToken.objects.filter(username=username).delete()
            otp = generate_and_send_otp(cached_data)
            return Response({
                'Message': 'A new OTP has been sent to your email address',
                'data': { 'otp_test' :  otp.otp_code}
                }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': f'User with this username : {username} Not Found!'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f"Email sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SignInView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=SingInSerializer,
        responses={
            200: "Successfully signed in",
            400: "Bad request (e.g., invalid data, missing required fields)",
            401: "Unauthorized (e.g., incorrect credentials)",
            403: "Forbidden (e.g., user not verified)"
        }
    )
    def post(self, request):
        serializer = SingInSerializer(data=request.data)
        if serializer.is_valid():
            username_or_email = serializer.validated_data['username_or_email']
            password = serializer.validated_data['password']

            user = User.objects.get(Q(username=username_or_email) | Q(email=username_or_email))

            if not user or not user.check_password(password):
                return Response({
                    'error': 'Invalid credentials'
                    }, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_verified:
                return Response({
                    'error': 'Please verify your email address before signing in.'
                    }, status=status.HTTP_403_FORBIDDEN)

            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'Successfully signed in',
                'data' : {**tokens},
                }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignOutView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type='object',
            properties={
                'refresh_token': openapi.Schema(
                    type='string',
                    description='The refresh token to be revoked.',
                    required=['refresh_token'],
                ),
            },
        ),
        responses={
            200: "Successfully signed out.",
            400: "Bad request (e.g., missing refresh token, invalid token).",
            500: "Internal server error (e.g., token blacklist failure).",
        }
    )
    def post(self, request):
        refresh_token = request.data["refresh_token"]
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()

                return Response({
                    'message': 'Successfully signed out'
                    }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({
                    'error': f"Failed to sign out: {str(e)}"
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'error': 'Refresh token is required'
                }, status=status.HTTP_400_BAD_REQUEST)
