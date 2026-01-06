from django.db import models
from django.contrib.auth import get_user_model
from categories.models import Category
from tags.models import Tag
from django.utils import timezone


User = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300, help_text="Short description for main page")
    body = models.TextField(help_text="Full content text")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Order by creation date (newest first)

    def __str__(self):
        return self.title
