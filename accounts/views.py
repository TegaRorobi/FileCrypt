from rest_framework import viewsets, mixins, status, permissions
from django.contrib.auth import get_user_model
from .serializers import (
    UserSerializer,
)

viewsets.ModelViewSet

User = get_user_model()


class UsersViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):

    queryset = User.objects.order_by('-id')
    serializer_class = UserSerializer


    def get_permissions(self):
        if self.action in ('create', 'list'):
            return [permissions.AllowAny()]
        return  [permissions.IsAuthenticated()]

    def get_object(self):
        return self.request.user
