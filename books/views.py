# django
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
from authentication.utils import generate_and_send_otp, SwaggerResponse
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
                description='Use "true" to retrieve read books(/book/?is_read=true)',
                type=bool,
                enum=['true', 'false']
            ),
            OpenApiParameter(
                name='is_favorite',
                required=False,
                description='Use "true" to retrieve favorite books (/book/?is_favorite=true)',
                type=bool,
                enum=['true', 'false']
            ),
            OpenApiParameter(
                name='title',
                required=False,
                description='Search books by book title (/book/?title=sport).',
                type=str,
            ),
            OpenApiParameter(
                name='category',
                required=False,
                description='Filter books by category name (/book/?category=romance).',
                type=str,
            ),
            OpenApiParameter(
                name='page',
                required=False,
                description='Page number for pagination (/book/?page=1).',
                type=int,
            ),
            OpenApiParameter(
                name='limit',
                required=False,
                description='Number of items per page (/book/?limit=10).',
                type=int,
            )
        ],
        description="Use query parameters to filter the books. Both parameters are optional. If only one is provided, it will filter based on that criterion only."
    )
    def get(self, request):
        user = request.user
        is_read = request.query_params.get('is_read', None)
        is_favorite = request.query_params.get('is_favorite', None)
        title = request.query_params.get('title', None)
        category_name = request.query_params.get('category', None)
        page_number = request.query_params.get('page', 1)
        limit_page = request.query_params.get('limit', 10)

        queryset = Book.objects.filter(user=user)

        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')

        if is_favorite is not None:
            queryset = queryset.filter(is_favorite=is_favorite.lower() == 'true')

        if title:
            queryset = queryset.filter(title__icontains=title)

        if category_name is not None:
            queryset = queryset.filter(category=category_name)

        paginator = Paginator(queryset, int(limit_page))

        try:
            paginated_queryset = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_queryset = paginator.page(1)
        except EmptyPage:
            paginated_queryset = paginator.page(paginator.num_pages)

        serializer = BookSerializer(paginated_queryset, many=True)

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
            if image:
                username = request.user.username
                title = serializer.validated_data['title']
                supabase_image_url = upload_to_supabase(image, username, title)
                serializer.validated_data['image_url'] = supabase_image_url
            else:
                # If image is not provided, set image_url to an empty string
                serializer.validated_data['image_url'] = ''

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

    @extend_schema(
        responses=BookSerializer,
        summary="Get a book",
        description="Retrieve details of a book by providing its ID.",
    )
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

    @extend_schema(
        request=CreateBookSerializer,
        responses=BookSerializer,
        summary="Update a book",
        description="Update details of a book by providing its ID and new data.",
    )
    def patch(self, request, pk):
        book = Book.objects.filter(pk=pk, user=request.user).first()
        if not book:
            raise NotFound({'error': f"Book with ID: {pk} not found."})

        serializer = CreateBookSerializer(instance=book, data=request.data, context={
            'request': request}, partial=True)
        if serializer.is_valid():
            image = request.FILES.get('image_url')
            if image:
                username = request.user.username
                title = serializer.validated_data['title']
                supabase_image_url = upload_to_supabase(image, username, title)
                serializer.validated_data['image_url'] = supabase_image_url
            else:
                # If image is not provided, set image_url to an empty string
                serializer.validated_data['image_url'] = ''

            serializer.save()
            serialized_book = BookSerializer(book)
            return Response({
                "message": "Book updated successfully",
                "data": serialized_book.data
            }, status=status.HTTP_200_OK)
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        summary="Delete a book",
        description="Delete a book by providing its ID.",
        responses={
            204: SwaggerResponse.NO_CONTENT,
            404: SwaggerResponse.NOT_FOUND
        },
    )
    def delete(self, request, pk):
        book = Book.objects.filter(pk=pk, user=request.user).first()
        if not book:
            raise NotFound({'error': f"Book with ID: {pk} not found for current user"})

        book_data = BookSerializer(book).data
        book.delete()

        return Response({
            "message": "Book deleted successfully",
            "data": book_data},
            status=status.HTTP_200_OK
        )
