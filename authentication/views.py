# django
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
# apps
from .serializers import UserSerializer
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
            serializer.save()
            # Handle successful signup (e.g., redirect to login page, send confirmation email)
            return Response({'message': 'User created successfully.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

