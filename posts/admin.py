from django.contrib import admin
from . import models

# class PostsLikedInline(admin.TabularInline):
#     model = models.PostsLiked

admin.site.register(models.Post)
