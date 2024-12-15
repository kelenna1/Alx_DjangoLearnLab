from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.response import Response
from.models import Post, Like
from notifications.models import Notification
from rest_framework.permissions import IsAuthenticated


# Create your views here.
'''class IsAuthorOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user'''
    
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, '''IsAuthorOrReadonly''']
    
    def perform_create(self, serializer):
        print("Validated data:", serializer.validated_data)
        print("Request user:", self.request.user)
        serializer.save(author=self.request.user)
        
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, '''IsAuthorOrReadonly''']
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')
    
class LikePostView(generics.GenericAPIView):
    permission_classes =[permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            return Response({'error': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST) #when a user tries to like a post more than once
    #Creating a Notification
        Notification.objects.create(recipient = post.author, actor = request.user, verb='Liked your post',target=post)
        return Response({'success': f'You liked the post "{post.title}"'}, status=status.HTTP_200_OK)
    
class UnlikePostView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
        except Like.DoesNotExist:
            return Response({'error': 'You have not liked this post.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'You have unliked the post "{post.title}"'}, status=status.HTTP_200_OK)
