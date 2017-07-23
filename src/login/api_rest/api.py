from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

from login.api_rest.permissions import UsersPermission
from login.api_rest.serializers import UsersListSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (UsersPermission,)

    def get_serializer_class(self):
        return UsersListSerializer if self.action == "list" else UserSerializer

