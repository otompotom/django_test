from django.db import models
from django.urls import reverse
from django.conf import settings

from rest_framework.reverse import reverse as api_reverse

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    likes = models.ManyToManyField(User, through="PostsLiked")  # post.likes.count() bi trebalo da vrati broj lajkova

    def __str__(self):
        return self.message

    def get_absolute_url(self):
        return reverse("posts:single", kwargs={"username": self.user.username, "pk": self.pk})

    def get_api_url(self, request=None):
        return api_reverse("api-posts:post-rud", kwargs={'pk': self.pk}, request=request)

    def get_likes_count(self):
        return self.likes.count()

    def get_likes_list(self):
        user_list = [likes_obj.user.username for likes_obj in self.likes.all()]
        for likes_obj in self.likes:
            user_list.append(likes_obj.user.username)
        return user_list


    @property
    def owner(self):
        return self.user

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]


class PostsLiked(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="like_users")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')