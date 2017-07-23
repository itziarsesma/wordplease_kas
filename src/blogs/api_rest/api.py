from django.contrib.auth.models import User
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.viewsets import ModelViewSet

from blogs.api_rest.permissions import PostsPermission
from blogs.api_rest.serializers import BlogSerializer, PostsListSerializer, PostSerializer
from blogs.models import Post


class BlogsAPI(ListAPIView):
    queryset = User.objects.all().values('username')
    serializer_class = BlogSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("username", )
    ordering_fields = ("username", )


class PostViewSet(ModelViewSet):
    permission_classes = (PostsPermission,)
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ("title", "body")
    ordering_fields = ("title", "publish_at")

    def get_serializer_class(self):
        if self.action == "list":
                return PostsListSerializer
        else:
            return PostSerializer

    def get_queryset(self):
        if "username" in self.kwargs:
            user = User.objects.get(username=self.kwargs.get("username"))
            if self.request.user.is_superuser or self.request.user == user:
                queryset = Post.objects.select_related().filter(owner=user).order_by('-publish_at')
            else:
                queryset = Post.objects.select_related().filter(owner=user).exclude(publish_at__isnull=True).order_by('-publish_at')
            return queryset
        elif "pk" in self.kwargs:
            queryset = Post.objects.select_related().filter(pk=self.kwargs.get("pk"))
            return queryset
        else:
            return None

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)