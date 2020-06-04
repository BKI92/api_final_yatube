import django_filters
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Create your views here.
from rest_framework import viewsets, status, generics, filters
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.response import Response

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
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username', ]

    def perform_create(self, serializer):
        following = User.objects.get(
            username=self.request.data.get('following'))
        serializer.save(user=self.request.user, following=following)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        following_username = request.data.get('following')
        if request.user.username != following_username:
            if User.objects.filter(username=following_username):
                target_user = User.objects.get(username=following_username)
                if not Follow.objects.filter(user=request.user,
                                             following=target_user):
                    self.perform_create(serializer)
                    headers = self.get_success_headers(serializer.data)
                    return Response(serializer.data,
                                    status=status.HTTP_201_CREATED,
                                    headers=headers)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
