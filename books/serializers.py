from rest_framework import serializers
from .models import Book
from categories.models import Category
from categories.serializers import CategorySerializer

class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'created_at', 'image_url', 'is_read', 'is_favorite', 'user', 'category']



class CreateBookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category', write_only=True)

    class Meta:
        model = Book
        fields = ['title', 'author', 'image_url', 'category_name', 'is_read', 'is_favorite']

    def validate_category_name(self, value):
        try:
            category = Category.objects.get(name=value)
            return category
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category: {value} does not exist.")

    def create(self, validated_data):
        category_name = validated_data.pop('category')
        category = self.validate_category_name(category_name)
        validated_data['category'] = category
        return super().create(validated_data)