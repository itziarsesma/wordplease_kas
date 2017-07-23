from rest_framework import serializers
from rest_framework.reverse import reverse

from blogs.models import Post


class BlogSerializer(serializers.Serializer):

    username = serializers.CharField()
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return self.context.get('request').build_absolute_uri(reverse('user_posts_list', args=[obj.get('username')]))


class PostsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("id", "title", "media_url", "intro", "publish_at")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('owner',)