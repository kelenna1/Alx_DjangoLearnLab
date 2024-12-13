from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.Serializer):
    author =serializers.ReadOnlyField(source= 'author.username')


    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']

class CommentSerializer(serializers.Serializer):
    author = serializers.ReadOnlyField(source ='author.username')
    post_title = serializers.ReadOnlyField(source = 'post.title')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'post', 'post_title', 'content', 'created_at', 'updated_at']