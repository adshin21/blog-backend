from django.conf import settings
from .models import Blog, Tag
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q
from random import shuffle
from .serializers import (
    PostListViewSerializer,
    PostDetailViewSerializer,
    PostCreateandUpdateViewSerializer,
    TagSerializer
)
from secrets import token_hex


import boto3
import requests
from contextlib import closing
S3_BUCKET = settings.AWS_STORAGE_BUCKET_NAME
region = settings.AWS_STORAGE_BUCKET_REGION


class PostListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostListViewSerializer
    permission_classes = (AllowAny, )


class PostDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostDetailViewSerializer
    lookup_field = 'slug'
    permission_classes = (IsOwnerOrReadOnly, )


class PostCreateView(generics.CreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostCreateandUpdateViewSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostUpdateView(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostCreateandUpdateViewSerializer
    lookup_field = 'slug'


class PostDestroyView(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostCreateandUpdateViewSerializer
    lookup_field = 'slug'


class GetTagViews(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny, )

    def paginate_queryset(self, queryset, view=None):
        return None


class PostRecommendationView(views.APIView):

    permission_classes = (AllowAny, )
    def post(self, request):

        tag_list, slug = request.data['tags'], request.data['slug']
        tags = [i['name'] for i in tag_list]
        tag_based = Blog.objects.filter(tags__name__in=tags).values("title", "slug").distinct()
        tag_based_list = list(tag_based)
        tag_based_list = filter(lambda x: x['slug'] != slug, tag_based_list)
        tag_based_list = list(tag_based_list)
        shuffle(tag_based_list)
        if len(tag_based_list) >= 3:
            return Response(
                data=tag_based_list,
                status=200
            )

        queries = [Q(title__icontains=tag) for tag in tags]

        query = queries.pop()

        for item in queries:
            query |= item

        title_based = Blog.objects.filter(query).values("title", "slug").distinct()
        title_based_list = list(title_based)
        title_based_list = filter(lambda x: x['slug'] != slug, title_based_list)
        tag_based_list = list(tag_based_list)

        res = [*tag_based_list, *title_based_list]
        shuffle(res)
        return Response(
            data=res,
            status=200
        )


class UploadImage(views.APIView):

    permission_classes = (AllowAny, )

    def post(self, request):

        file = ""
        fileName = ""

        try:
            file = request.FILES['image']
            fileName = token_hex(10) + '__' + file.name
        except:
            url = request.data.get("url", None)
            fileName = token_hex(10) + '__' + url.split('/')[-1]
            with closing(requests.get(url, stream=True, verify=False)) as res:
                file = res.content

        s3 = boto3.resource(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_STORAGE_BUCKET_REGION
        )
        s3.Bucket(S3_BUCKET).put_object(
            Body=file,
            Key=fileName,
            ACL='public-read'
        )
        url = "https:{0}.s3.{1}.amazonaws.com/{2}".format(
            S3_BUCKET,
            region,
            fileName
        )

        return Response({
            "file": {
                'url': url,
            },
            "success": 1
        })
