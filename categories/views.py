# django
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import Http404
# drf
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
# app
from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer, CategoryCreateSerializer
from books.models import Book
# swagger
from drf_spectacular.utils import OpenApiExample, extend_schema


class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get all categories",
        description="This allows authenticated users to retrieve all categories that belong to them",
        responses=CategorySerializer
    )
    def get(self, request):
        user = request.user  # Retrieve the authenticated user
        categories = Category.objects.filter(user=user)  # Filter categories for the authenticated user
        serializer = CategorySerializer(categories, many=True)

        return Response(
            {
                "message": "Categories retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Create a category",
        description="This allows authenticated users to create a new category.",
        request=CategorySerializer,
        responses={201: CategorySerializer}
    )
    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "Category created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get a category by ID",
        description="This allows authenticated users to retrieve a specific category by its ID.",
        responses=CategoryDetailSerializer
    )
    def get(self, request, pk):
        category = Category.objects.filter(pk=pk, user=request.user).first()
        if not category:
            raise NotFound({'error': f"Category with ID: {pk} not found."})

        serializer = CategoryDetailSerializer(category)

        return Response(
            {
                "message": "Category retrieved successfully",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Update a category",
        description="This allows authenticated users to update a category by its ID.",
        request=CategoryDetailSerializer,
        responses=CategoryDetailSerializer
    )
    def put(self, request, pk):
        category = Category.objects.filter(pk=pk, user=request.user).first()
        if not category:
            raise NotFound({'error': f"Category with ID: {pk} not found."})

        serializer = CategoryDetailSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Category updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a category",
        description="This allows authenticated users to delete a category by its ID.",
        responses={204: "No Content"}
    )
    def delete(self, request, pk):
        category = Category.objects.filter(pk=pk, user=request.user).first()
        if not category:
            raise NotFound({'error': f"Category with ID: {pk} not found."})

        if Book.objects.filter(category=category, user=request.user).exists():
            return Response(
                {"error": "This category is being used in one or more books. Remove the association before deleting the category."},
                status=status.HTTP_400_BAD_REQUEST
            )

        category.delete()
        return Response({
            "message":  "Category deleted successfully"},
            status=status.HTTP_204_NO_CONTENT)
