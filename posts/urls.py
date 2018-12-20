from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.ListPosts.as_view(), name='all'),
    path('new/', views.CreatePost.as_view(), name='create'),
    path('by/<str:username>/<int:pk>', views.SinglePost.as_view(), name='single'),
    path('by/<str:username>/', views.UserPosts.as_view(), name = 'for_user'),
    path('delete/<int:pk>', views.DeletePost.as_view(), name='delete'),
    path('like/<int:pk>', views.LikePost.as_view(), name='like'),
    path('unlike/<int:pk>', views.UnlikePost.as_view(), name='unlike'),

]