from django.urls import path, re_path
from .views import MyProfileView


urlpatterns = [
    path('', MyProfileView.as_view()),
]