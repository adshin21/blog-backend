from rest_framework import serializers
from .models import (
    Blog,
    Tag
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostListViewSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Blog
        fields = (
            'author',
            'title',
            'slug',
            'content',
            'published_at',
            'tags'
        )


class PostDetailViewSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Blog
        fields = (
            'author',
            'title',
            'slug',
            'content',
            'published_at',
            'draft',
            'tags'
        )


class PostCreateandUpdateViewSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many=True, read_only=False)

    class Meta:
        model = Blog
        fields = (
            'title',
            'content',
            'slug',
            'published_at',
            'tags'
        )

        read_only_fields = ('slug',)

    def create(self, validated_data):
        tag_data = validated_data.pop('tags')

        blog = Blog.objects.create(**validated_data)

        for tag in tag_data:
            tag, created = Tag.objects.get_or_create(**tag)
            blog.tags.add(tag)
        return blog

    def update(self, instance, validated_data):

        for existing_tag in instance.tags.all():
            instance.tags.remove(existing_tag)

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.draft = validated_data.get('draft', instance.draft)

        tag_data = validated_data.pop('tags')
        for tag in tag_data:
            tag, created = Tag.objects.get_or_create(**tag)
            instance.tags.add(tag)

        instance.save()
        return instance
