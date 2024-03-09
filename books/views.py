# django
from django.shortcuts import render
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotFound
# apps
from .models import Book
from .serializers import BookSerializer, CreateBookSerializer
from categories.models import Category
from .utils import upload_to_supabase
# swagger
from drf_spectacular.utils import OpenApiExample, extend_schema, OpenApiParameter
from django.views.decorators.csrf import csrf_exempt


class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=BookSerializer,
        summary="Get filtered books",
        parameters=[
            OpenApiParameter(
                name='is_read',
                required=False,
                description='Use "true" to retrieve read books(/books/?is_read=true)',
                type=bool,
                enum=['true', 'false']
            ),
            OpenApiParameter(
                name='is_favorite',
                required=False,
                description='Use "true" to retrieve favorite books (/books/?is_favorite=true)',
                type=bool,
                enum=['true', 'false']
            ),
            OpenApiParameter(
                name='title',
                required=False,
                description='Search books by book title (/books/?title=sport).',
                type=str,
            ),
            OpenApiParameter(
                name='category',
                required=False,
                description='Filter books by category name (/books/?category=romance).',
                type=str,
            )
        ],
        description="Use query parameters to filter the books. Both parameters are optional. If only one is provided, it will filter based on that criterion only."
    )
    def get(self, request):
        user = request.user
        is_read = request.query_params.get('is_read', 'false').lower() == 'true'
        is_favorite = request.query_params.get('is_favorite', 'false').lower() == 'true'
        title = request.query_params.get('title', None)
        category_name = request.query_params.get('category', None)

        queryset = Book.objects.filter(user=user)

        if is_read is not False:
            queryset = queryset.filter(is_read=is_read)

        if is_favorite is not False:
            queryset = queryset.filter(is_favorite=is_favorite)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if category_name is not None:
            queryset = queryset.filter(category=category_name)

        serializer = BookSerializer(queryset, many=True)

        return Response(
            {
                "message": "Books retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        request=CreateBookSerializer,
        summary="Create a new book",
        description="Create a new book by providing the required information.",
        responses=CreateBookSerializer
    )
    # @csrf_exempt
    def post(self, request):
        serializer = CreateBookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            image = request.FILES.get('image_url')
            username = request.user.username
            title = serializer.validated_data['title']

            if not image:
                return Response({
                    "error": "No image file uploaded."
                }, status=status.HTTP_400_BAD_REQUEST)

            if image:
                supabase_image_url = upload_to_supabase(image, username, title)
                serializer.validated_data['image_url'] = supabase_image_url

            book = serializer.save(user=request.user)
            serializer = BookSerializer(book, many=True)
            serialized_book = BookSerializer(book)

            return Response({
                "message": "Book created successfully",
                "data": serialized_book.data
            }, status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        book = Book.objects.filter(pk=pk, user=request.user).first()
        if not book:
            raise NotFound({'error': f"Book with ID: {pk} not found for current user"})

        serializer = BookSerializer(book)

        return Response(
            {
                "message": "Category retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, pk):
        book = Book.objects.filter(pk=pk, user=request.user).first()
        if not book:
            raise NotFound({'error': f"Book with ID: {pk} not found for current user"})

        book.delete()

        return Response(
            {"message": "Book deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )
