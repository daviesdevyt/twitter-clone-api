from rest_framework import serializers
from .models import User, Post, Comment, Profile

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = '__all__'