from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'), # List posts at the app root
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'), # Detail view
    path('post/new/', PostCreateView.as_view(), name='post_new'), # Create post
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'), # Edit post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'), # Delete post
]