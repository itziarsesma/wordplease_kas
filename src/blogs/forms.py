from django import forms
from django.forms import SelectMultiple

from blogs.models import Post, Genre


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'intro', 'body', 'media_url', 'genres', "publish_at"]