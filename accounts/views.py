from django.shortcuts import render

# Create your views here.


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.models import User
from .serializers import UserSerializer


class MyProfileView(APIView):
  permission_classes = [IsAuthenticated]


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
