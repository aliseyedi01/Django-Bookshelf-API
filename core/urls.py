from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# drf
from rest_framework import permissions
# Swagger
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)





urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('books.urls')),
    path('auth/', include('authentication.urls')),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
]

urlpatterns += staticfiles_urlpatterns()


