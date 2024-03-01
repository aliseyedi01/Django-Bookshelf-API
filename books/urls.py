from django.urls import path, re_path
from .views import BookListView


urlpatterns = [
    path('', BookListView.as_view(), name='book-list'),
]