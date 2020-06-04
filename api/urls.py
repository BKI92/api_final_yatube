from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from api.views import PostViewSet, CommentViewSet, FollowViewSet, GroupViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
# router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comments')
commets_router = routers.NestedSimpleRouter(router, r'posts', lookup='posts')
commets_router.register(r'comments', CommentViewSet, basename='comments')
# router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(commets_router.urls)),
    path('follow/', FollowViewSet.as_view(), name='follow'),
    path('group/', GroupViewSet.as_view(), name='group')
]
