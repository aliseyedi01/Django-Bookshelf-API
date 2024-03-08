from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.models import User
from .serializers import UserSerializer
from authentication.utils import  SwaggerResponse

class MyProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Retrieve information about the authenticated user's profile",
        summary="Get user information",
        responses={
            200 : UserSerializer,
            404 : SwaggerResponse.NOT_FOUND,
        }
    )
    def get(self, request):
        username = request.user.username

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)

        return Response({
            "message": "This is your profile",
            "data":serializer.data
            },status=status.HTTP_201_CREATED
        )
