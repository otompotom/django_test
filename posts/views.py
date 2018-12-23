from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.views import generic
from django.urls import reverse_lazy, reverse
from .models import Post, PostsLiked
from django.contrib import messages

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.


class CreatePost(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ("message",)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class SinglePost(generic.DetailView):
    model = Post


class ListPosts(generic.ListView):
    model = Post


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = Post
    select_related = ("user",) # NE RADI KAD JE OVO ZAKOMENTARISANO ...
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)

class UserPosts(generic.ListView):
    model = Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context

class LikePost(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        # return reverse("posts:single", kwargs={"username": self.kwargs.get("username"), "pk": self.kwargs.get("pk")})
        return reverse("posts:all")

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))

        try:
            PostsLiked.objects.create(user=self.request.user, post=post)

        except IntegrityError:
            messages.warning(self.request, "AAAAAAAAAAAAAAAAAAAAA")

        else:
            messages.success(self.request, "You have successfully liked a post")

        return super().get(request, *args, **kwargs)


class UnlikePost(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        # return reverse("posts:single", kwargs={"username": self.kwargs.get("username"), "pk": self.kwargs.get("pk")})
        return reverse("posts:all")

    def get(self, request, *args, **kwargs):

        try:
            post_liked_by_user_relationship = PostsLiked.objects.filter(
                user=self.request.user,
                post__pk=self.kwargs.get("pk")
            ).get()

        except PostsLiked.DoesNotExist:
            messages.warning(
                self.request,
                "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
            )
        else:
            post_liked_by_user_relationship.delete()
            messages.success(
                self.request,
                "You have successfully liked a post."
            )
        return super().get(request, *args, **kwargs)