from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.models import User
from .serializers import UserSerializer,UpdateUserSerializer
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

    @extend_schema(
        description="Update the authenticated user's profile",
        summary="Update user information",
        responses={
            200: UpdateUserSerializer,
            400: "Invalid request data",
            404: SwaggerResponse.NOT_FOUND,
        },
        request=UpdateUserSerializer
    )
    def put(self, request):
        username = request.user.username

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User information updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)