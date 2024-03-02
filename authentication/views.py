# django
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.messages import success, warning
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
# apps
from .serializers import UserSerializer
from .models import OtpToken
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
            # user = serializer.validated_data['email']
            otp = OtpToken.objects.create(user=user, expires_at=timezone.now() + timezone.timedelta(minutes=5))
            message = f"""
                Hi {user}, here is your OTP {otp.otp_code}
                It expires in 5 minutes, use the url below to redirect back to the website
                http://127.0.0.1:8000/verify-email/{user}
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