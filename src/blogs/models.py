from django.contrib.auth.models import User
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=150)
    intro = models.CharField(max_length=500)
    body = models.TextField()
    media_url = models.URLField(blank=True, null=True)
    publish_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    genres = models.ManyToManyField(Genre)
    owner = models.ForeignKey(User, related_name="published_by")

    def __str__(self):
        return self.title
