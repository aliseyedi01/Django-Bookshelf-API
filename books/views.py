# django
from django.shortcuts import render
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
# apps
from .models import Book
from .serializers import BookSerializer



class BookListView(APIView):
    def get(self, request):
        user_books = Book.objects.all()
        serializer = BookSerializer(user_books, many=True)
        return Response(serializer.data)