from rest_framework import serializers
from .models import Book
from categories.models import Category
from categories.serializers import CategorySerializer
from .utils import upload_to_supabase
from authentication.serializers import BaseCustomSerializer


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'image_url', 'category',
                  'is_read', 'is_favorite', 'created_at']


class CreateBookSerializer(BaseCustomSerializer, serializers.ModelSerializer):
    category_name = serializers.CharField(source='category', write_only=True)
    image_url = serializers.ImageField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Book
        fields = ['title', 'author', 'image_url', 'category_name', 'is_read', 'is_favorite']

    def validate_category_name(self, value):
        user = self.context['request'].user
        try:
            category = Category.objects.get(name=value, user=user)
            return category.name
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category: {value} does not exist for the current user.")

    def validate_title(self, value):
        user = self.context['request'].user

        if self.instance and self.instance.title == value:
            return value

        if Book.objects.filter(title=value, user=user).exists():
            raise serializers.ValidationError(
                f"A book with the title '{value}' already exists for the current user.")
        return value
