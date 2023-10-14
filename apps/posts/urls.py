from django.urls import path

from .views import PostListAPIView, PostCreateAPIView, PostRetrieveUpdateDestroyView, PostCommentListAPIView, \
    PostCommentCreateView, CommentListCreateAPIView, PostLikeListView, CommentRetrieveView, CommentLikeListView, \
    PostLikeAPIView, CommentLikeAPIView

urlpatterns = [
    path('list/', PostListAPIView.as_view(), ),
    path('create/', PostCreateAPIView.as_view(), ),
    path('<uuid:pk>/', PostRetrieveUpdateDestroyView.as_view(), ),
    path('<uuid:pk>/likes/', PostLikeListView.as_view(), ),
    path('<uuid:pk>/comments/', PostCommentListAPIView.as_view(), ),
    path('<uuid:pk>/comment/create/', PostCommentCreateView.as_view(), ),

    path('comments/', CommentListCreateAPIView.as_view(), ),
    path('comments/<uuid:pk>/', CommentRetrieveView.as_view(), ),
    path('comments/<uuid:pk>/likes/', CommentLikeListView.as_view(), ),

    path('<uuid:pk>/like-dislike/', PostLikeAPIView.as_view(), ),
    path('<uuid:pk>/post-like-dislike/', PostLikeAPIView.as_view(), ),
    path('comments/<uuid:pk>/comment-like-dislike/', CommentLikeAPIView.as_view(), ),
]
