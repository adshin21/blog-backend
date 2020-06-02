from .models import Blog
from rest_framework import generics

from .serializers import (
    PostListViewSerializer,
    PostDetailViewSerializer,
    PostCreateandUpdateViewSerializer
)


class PostListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostListViewSerializer


class PostDetailView(generics.RetrieveAPIView):
    queryset = Blog.objects.all()
    serializer_class = PostDetailViewSerializer
    lookup_field = 'slug'


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
