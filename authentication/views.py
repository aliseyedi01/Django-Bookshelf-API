# django
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.messages import success, warning
from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
# apps
from .serializers import UserSerializer , ResendOtpSerializer
from .models import OtpToken,User
# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



class SignUpView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201:UserSerializer(many=True),
            400: 'Bad request (e.g., invalid data, missing required fields)',
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate and send OTP
            otp = OtpToken.objects.create(user=user, expires_at=timezone.now() + timezone.timedelta(minutes=5))
            message = f"""
                Hi {user}, here is your OTP {otp.otp_code}
                It expires in 5 minutes, use the url below to redirect back to the website
                http://127.0.0.1:8000/verify-email/{otp.user.username}
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
            return Response({'error': 'OTP has expired. Please request a new one.'}, status=status.HTTP_400_BAD_REQUEST)

        user.save()
        user_otp.delete()

        # Log in the user automatically (optional)
        # login(request, authenticate(username=username, password=user.password))

        return Response({'Message': 'Your account has been activated successfully!'} ,status=status.HTTP_200_OK)


class ResendOtpView(APIView):
    def post(self, request):
        serializer = ResendOtpSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_email = request.data["email"]
        user = User.objects.get(email=user_email)
        otp = OtpToken.objects.create(user=user, expires_at=timezone.now() + timezone.timedelta(minutes=5))

        message = f"""
            Hi {user.username}, here is your OTP {otp.otp_code}
            It expires in 5 minutes, use the url below to redirect back to the website
            http://127.0.0.1:8000/verify-email/{user.username}
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
