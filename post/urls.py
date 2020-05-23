from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDestroyView
)


urlpatterns = [
    path(
        '',
        PostListView.as_view(),
        name="post-list-view"
    ),
    path(
        'create/',
        PostCreateView.as_view(),
        name="post-create-view"
    ),
    path(
        '<str:slug>/',
        PostDetailView.as_view(),
        name="post-detail-view"
    ),
    path(
        '<str:slug>/edit/',
        PostDetailView.as_view(),
        name="post-update-view"
    ),
    path(
        '<str:slug>/delete/',
        PostDestroyView.as_view(),
        name="post-destroy-view"
    ),

]