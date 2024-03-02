from rest_framework import serializers
from .models import BlogPost, BlogImage, Profile, Team, Tag, Experience


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class BlogTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'value']


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image']


class ExperienceSerializer(serializers.ModelSerializer):
    tags = BlogTagSerializer(many=True, read_only=True)

    class Meta:
        model = Experience
        fields = ['number', 'title', 'info', 'tags']


class BlogPostSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)
    tags = BlogTagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'info', 'price', 'created_at', 'updated_at', 'images', 'tags']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['company', 'address', 'phone', 'whatsapp_number', 'email', 'instagram_url']
        read_only_fields = ('id',)


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['image', 'name', 'position']