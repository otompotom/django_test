from django.urls import path

from .views import PostRudView, PostAPIView

app_name = 'api-posts'

urlpatterns = [
    path('', PostAPIView.as_view(), name='post-listcreate'),
    path('<int:pk>', PostRudView.as_view(), name='post-rud')
]