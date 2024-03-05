# django
from django.shortcuts import render
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# apps
from .models import Book
from .serializers import BookSerializer
# swagger
from drf_spectacular.utils import OpenApiExample, extend_schema


class BookListView(APIView):
    permission_classes = [IsAuthenticated]
    # @swagger_auto_schema(responses={200: BookSerializer(many=True)})
    @extend_schema(
        request=BookSerializer
    )
    def get(self, request):
        user_books = Book.objects.all()
        serializer = BookSerializer(user_books, many=True)
        return Response(serializer.data)

