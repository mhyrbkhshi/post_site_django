from django.urls import path 
from .views import IndexView, PostListView, TagListView, PopularPostView, post_like, TagDetailView, post_delete_view, PostUpdateView, post_detail_view, comment_delete, post_create_view


urlpatterns = [
    path('', IndexView.as_view(), name="home-index"),
    path('post/list', PostListView.as_view(), name="post-list"),
    path('post/create', post_create_view, name='post-create'),
    path('post/popular/list', PopularPostView.as_view(), name="post-popular-list"),
    path('tag/list', TagListView.as_view(), name="tag-list"),
    path('tag/<str:tag_slug>', TagDetailView.as_view(), name="tag-detail"),
    path('post/<str:post_slug>', post_detail_view, name='post-detail'),
    # add or remove user like from post entry 
    path('post/<str:post_slug>/like', post_like, name='post-like'),
    path('post/<str:post_slug>/delete', post_delete_view, name='post-delete'),
    path('post/<str:post_slug>/update', PostUpdateView.as_view(), name='post-update'),
    path('comment/<int:comment_pk>/delete', comment_delete, name='comment-delete'),
]
