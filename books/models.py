from django.db import models
import uuid

class Book(models.Model):
    uuid = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, unique=True)
    author = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField(max_length=2000)


    def __str__(self):
        return self.title
