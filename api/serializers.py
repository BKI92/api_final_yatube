from rest_framework import serializers

from .models import Post, Comment, Follow, Group, User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    following = serializers.CharField(source='following.username')

    class Meta:
        fields = ('user', 'following')
        model = Follow

    def validate(self, data):
        user = self.context['request'].user
        following_name = self.context['request'].data['following']
        if not User.objects.filter(username=following_name):
            raise serializers.ValidationError(
                f"User with name {following_name} don't exist")
        if user.username == following_name:
            raise serializers.ValidationError(
                f"You could not follow on yourself")
        target_user = User.objects.get(username=following_name)
        if Follow.objects.filter(user=user, following=target_user):
            raise serializers.ValidationError(
                f"You already followed on {following_name}")
        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title',)
        model = Group
