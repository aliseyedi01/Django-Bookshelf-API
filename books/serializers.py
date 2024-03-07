from rest_framework import serializers
from .models import Book
from categories.serializers import CategorySerializer

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'created_at', 'image_url', 'is_read', 'is_favorite', 'user', 'category']

