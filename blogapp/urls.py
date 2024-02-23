from django.urls import path
from .views import BlogsView, CommentsView, LikesView, BlogCreateView, CommentWriteView, LikeView

urlpatterns = [
    path('blogs/', BlogsView.as_view(), name='blog-list'),
    path('upload/blog/', BlogCreateView.as_view(), name='blog-list'),
    path('like/<int:pk>/', LikeView.as_view(), name='like'),
    path('blog/likes/<int:pk>', LikesView.as_view(), name='like'),
    path('comment/', CommentsView.as_view(), name='comment'),
    path('comment/<int:pk>/', CommentWriteView.as_view(), name='comment')
]   
