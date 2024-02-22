from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Blog, Like, Comment
from .models import MyUser
from .serializers import CommentSerializer, BlogSerializer, LikesSerializer
from django.db.models import Q

class BlogsView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request, *args, **kwargs):
        tags = request.GET.get('tags', None)

        if tags:
            blogs = Blog.objects.filter(comment__tags__icontains=tags).distinct()
        else:
            blogs = Blog.objects.all()

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

class LikesView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        likes = Like.objects.all()
        serializer = LikesSerializer(likes, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = LikesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BlogCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        request.data['author'] = user.id
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            blog = serializer.save()
            return Response({'msg':'Blog Uploaded Successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CommentsView(APIView):

    def get(self, request, *args, **kwargs):
        blog_id = self.kwargs.get('blog_id')
        tags = request.GET.get('tags', None)
        
        if tags:
            comments = Comment.objects.filter(blog__id=blog_id, tags__icontains=tags)
        else:
            comments = Comment.objects.filter(blog__id=blog_id)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentWriteView(APIView):

    def post(self, request, *args, **kwargs):
        user = request.user
        blog_id = kwargs.get('pk')
        request.data['user'] = user.id
        request.data['blog'] = blog_id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)