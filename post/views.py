from .models import Blog
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q

from .serializers import (
    PostListViewSerializer,
    PostDetailViewSerializer,
    PostCreateandUpdateViewSerializer
)


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


class PostRecommendationView(views.APIView):

    permission_classes = (AllowAny, )
    def post(self, request):

        tag_list, slug = request.data['tags'], request.data['slug']
        tags = [i['name'] for i in tag_list]
        print('tags', tags, slug)
        tag_based = Blog.objects.filter(tags__name__in=tags).values("title", "slug").distinct()
        tag_based_list = list(tag_based)
        tag_based_list = filter(lambda x: x['slug'] != slug, tag_based_list)
        tag_based_list = list(tag_based_list)

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

        return Response(
            data=[*tag_based_list, *title_based_list],
            status=200
        )
