# django
from django.shortcuts import render
# drf
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# apps
from .models import Book
from .serializers import BookSerializer
# swagger
from drf_spectacular.utils import OpenApiExample, extend_schema , OpenApiParameter


class BookListView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses=BookSerializer,
        parameters=[
            OpenApiParameter(
                name='is_read',
                required=False,
                description='use "true" to retrieve read books(/books/?is_read=true)',
                type=bool,
                enum=['true', 'false']
            ),
            OpenApiParameter(
                name='is_favorite',
                required=False,
                description='use "true" to retrieve favorite books (/books/?is_favorite=true)',
                type=bool,
                enum=['true', 'false']
            )
        ],
       description="Use query parameters to filter the books. Both parameters are optional. If only one is provided, it will filter based on that criterion only."
    )
    def get(self, request):
        is_read = request.query_params.get('is_read', None)
        is_favorite = request.query_params.get('is_favorite', None)

        queryset = Book.objects.all()

        if is_read is not None:
            queryset = queryset.filter(is_read=is_read)

        if is_favorite is not None:
            queryset = queryset.filter(is_favorite=is_favorite)

        serializer = BookSerializer(queryset, many=True)

        return Response(
            {
                "message": "Books retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )