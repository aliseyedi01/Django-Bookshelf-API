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
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
# apps
from .serializers import SingUpSerializer , ResendOtpSerializer , SingInSerializer
from .models import OtpToken,User
# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class SignUpView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=SingUpSerializer,
        responses={
            201: openapi.Response(
                description="Account created successfully!",
                schema=SingUpSerializer(many=True),
            ),
            400: "Bad request (e.g., invalid data, missing required fields)",
        }
    )
    def post(self, request):
        serializer = SingUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate and send OTP
            otp = OtpToken.objects.create(user=user, expires_at=timezone.now() + timezone.timedelta(minutes=1))
            message = f"""
                Hi {user}, here is your OTP {otp.otp_code}
                It expires in 5 minutes, use the url below to redirect back to the website
                https://library-api-t70g.onrender.com/verify-email/{otp.user.username}
            """
            try:
                send_mail(
                    subject="Email Verification",
                    message=message,
                    from_email="aliotptest@gmail.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                user.delete()
                return Response({'error': f"Email sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'Message': 'Account created successfully! An OTP has been sent to your email for verification'} ,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyEmailView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type='object',
            properties={
                'otp_code': openapi.Schema(
                    type='string',
                    description='The OTP code sent to the user\'s email.',
                ),
            },
        ),
        responses={
            200:"Account activated successfully!",
            400: "Bad request (e.g., invalid OTP code, expired OTP)",
            404: "User with the provided username not found",
        }
    )
    def post(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': f'User with this username : {username} Not Found!'}, status=status.HTTP_404_NOT_FOUND)

        user_otp = OtpToken.objects.filter(user=user).order_by('-created_at').first()
        if not user_otp:
            return Response({'error': 'No OTP found for this user'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate OTP code
        if request.data.get('otp_code') != user_otp.otp_code:
            return Response({'error': 'Invalid OTP code'}, status=status.HTTP_400_BAD_REQUEST)

        # Check for expired OTP
        if user_otp.expires_at < now():
            user_otp.delete()
            # Generate and send a new OTP
            otp = OtpToken.objects.create(user=user, expires_at=timezone.now() + timezone.timedelta(minutes=1))
            message = f"""
                Hi {user}, here is your new OTP {otp.otp_code}
                It expires in 5 minutes, use the URL below to redirect back to the website
                https://library-api-t70g.onrender.com/verify-email/{user.username}
            """
            try:
                send_mail(
                    subject="Email Verification",
                    message=message,
                    from_email="aliotptest@gmail.com",
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({'error': f"Email sending failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'Message': 'OTP has expired , A new OTP has been sent to your email address'}, status=status.HTTP_200_OK)

        user.is_verified = True
        user.save()
        user_otp.delete()

        return Response({'Message': 'Your account has been activated successfully!'} ,status=status.HTTP_200_OK)


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

        user_email = request.data["email"]
        user = User.objects.get(email=user_email)
        otp = OtpToken.objects.create(user=user, expires_at=timezone.now() + timezone.timedelta(minutes=1))

        message = f"""
            Hi {user.username}, here is your OTP {otp.otp_code}
            It expires in 5 minutes, use the url below to redirect back to the website
            https://library-api-t70g.onrender.com/verify-email/{user.username}
        """
        try:
            send_mail(
                subject="Email Verification",
                message=message,
                from_email="aliotptest@gmail.com",
                recipient_list=[user.email],
                fail_silently=False,
            )
            return Response({'Message': 'A new OTP has been sent to your email address'}, status=status.HTTP_200_OK)
        except Exception as e:
            otp.delete()
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
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.is_verified:
                return Response({'error': 'Please verify your email address before signing in.'}, status=status.HTTP_403_FORBIDDEN)

            # Generate JWT tokens upon successful authentication
            access_token = str(AccessToken.for_user(user))
            refresh_token = str(RefreshToken.for_user(user))

            return Response({
                'message': 'Successfully signed in',
                'access_token': access_token,
                'refresh_token': refresh_token
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

                return Response({'message': 'Successfully signed out'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': f"Failed to sign out: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
