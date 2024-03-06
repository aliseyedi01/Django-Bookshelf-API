from django.db import models
from authentication.models import User
from categories.models import Category

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books',default=1)

    is_read = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)


    def __str__(self):
        return self.title
