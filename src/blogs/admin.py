from django.contrib import admin

from blogs.models import Post, Genre

admin.site.register(Post)
admin.site.register(Genre)
