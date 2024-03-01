from django.contrib import admin
from django.urls import path
from django.urls import path, include
# drf
from rest_framework import permissions
# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema Swagger
schema_view = get_schema_view(
	openapi.Info(
			title="📚 Book Library API",
			default_version='v1',
			description="**Book Library API (v1): CRUD, search, filter, integrate. \n By: @aliseyedi01** 💻",
			contact=openapi.Contact(name="My Github", url="https://github.com/aliseyedi01"),
	),
	public=True,
	permission_classes=(permissions.AllowAny,),
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('book/', include('books.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
	path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
	path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


