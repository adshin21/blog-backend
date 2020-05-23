from rest_framework import serializers
from .models import Blog


class PostListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'author',
            'title',
            'slug',
            'content',
            'updated_at',
            'published_at'
        )


class PostDetailViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'author',
            'title',
            'slug',
            'content',
            'updated_at',
            'published_at',
            'draft'
        )


class PostCreateandUpdateViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
            'title',
            'content',
            'delta',
            'published_at'
        )
