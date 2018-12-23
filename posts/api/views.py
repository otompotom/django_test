# generic

from django.db.models import Q
from rest_framework import generics, mixins

from posts.models import Post
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer


class PostAPIView(mixins.CreateModelMixin, generics.ListAPIView): # DetailView CreateView FormView
    lookup_field = 'pk'  # slug, id # url(r'?P<pk>\d+')
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class PostRudView(generics.RetrieveUpdateDestroyAPIView): # DetailView CreateView FormView
    lookup_field = 'pk' # slug, id # url(r'?P<pk>\d+')
    serializer_class = PostSerializer

    # overrides DEFAULT_PERMISSION_CLASSES iz settings.py
    permission_classes = [IsOwnerOrReadOnly]


    def get_queryset(self):
        return Post.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}

