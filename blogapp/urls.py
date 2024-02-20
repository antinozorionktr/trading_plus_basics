from django.urls import path
from .views import BlogsView, CommentsView, LikesView, BlogCreateView

urlpatterns = [
    path('blogs/', BlogsView.as_view(), name='blog-list'),
    path('upload/blog/', BlogCreateView.as_view(), name='blog-list'),
    path('like/<int:pk>/', LikesView.as_view(), name='like'),
    path('comment/<int:pk>/', CommentsView.as_view(), name='comment')
]
