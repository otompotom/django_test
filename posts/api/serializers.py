from rest_framework import serializers

from posts.models import Post, PostsLiked
from django.contrib.auth import get_user_model


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['username', ]
#
#
# class PostsLikedSerializer(serializers.ModelSerializer):
#     user = UserSerializer()
#
#     class Meta:
#         model = PostsLiked
#         fields = ['user', ]

class PostSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    # likes = PostsLikedSerializer(many=True, read_only=True)
    # likes_list = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'user',
            'message',
            'created_at',
            'likes_count',
        ]
        read_only_fields = ['id', 'user']


    def get_url(self, obj):
        request = self.context.get("request")
        return obj.get_api_url(request=request)

    # def get_message(self, obj):
    #     return 'test'

    def get_likes_count(self, obj):
        return obj.get_likes_count()

    # def get_likes_list(self, obj):
    #     return obj.get_likes_list()
