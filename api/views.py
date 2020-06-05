from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.serializers import PostSerializer, CommentSerializer, \
    FollowSerializer, GroupSerializer
from .models import Post, Comment, Follow, User, Group
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating,  editing and deleting posts instances.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        if not self.request.query_params.get('group'):
            return Post.objects.all()
        return Post.objects.filter(group=self.request.query_params.get('group'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    A viewset for getting, updating, posting and deleting comments instances.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_post(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post

    def get_queryset(self):
        queryset = Comment.objects.filter(post=self.get_post()).all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(generics.ListCreateAPIView):
    """
     A viewset for getting and creating follow instances.
     """
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username', ]

    def perform_create(self, serializer):
        following = User.objects.get(
            username=self.request.data.get('following'))
        serializer.save(user=self.request.user, following=following)


class GroupViewSet(generics.ListCreateAPIView):
    """
      A viewset for getting and creating group instances.
      """
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
