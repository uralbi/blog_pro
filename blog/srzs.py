from rest_framework import serializers
from .models import BlogPost, BlogImage, Profile, Team


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image']


class BlogPostSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'info', 'price', 'created_at', 'updated_at', 'images']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['company', 'address', 'phone', 'whatsapp_number', 'email', 'instagram_url', 'created_at']
        read_only_fields = ('id', 'created_at')


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['image', 'name', 'position']