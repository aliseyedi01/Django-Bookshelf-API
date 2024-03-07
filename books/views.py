# django
from django.shortcuts import render
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# apps
from .models import Book
from .serializers import BookSerializer , CreateBookSerializer
from categories.models import Category
# swagger
from drf_spectacular.utils import OpenApiExample, extend_schema , OpenApiParameter


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
        is_read = request.query_params.get('is_read', None)
        is_favorite = request.query_params.get('is_favorite', None)
        title = request.query_params.get('title', None)
        category_name = request.query_params.get('category')

        queryset = Book.objects.all()

        if is_read is not None:
            queryset = queryset.filter(is_read=is_read)

        if is_favorite is not None:
            queryset = queryset.filter(is_favorite=is_favorite)

        if title:
            queryset = queryset.filter(title__icontains=title)

        if category_name:
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                return Response({
                    "error": f"Category '{category_name}' does not exist."
                    },status=status.HTTP_404_NOT_FOUND)

            queryset = queryset.filter(category=category.id)


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
    def post(self, request):
        serializer = CreateBookSerializer(data=request.data)
        if serializer.is_valid():

            book = serializer.save(user=request.user)
            serializer  = BookSerializer(book, many=True)
            serialized_book = BookSerializer(book)

            return Response({
                "message": "Book created successfully",
                "data": serialized_book.data
                },status=status.HTTP_201_CREATED
            )
        return Response(
            { "error" : serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )