from rest_framework import viewsets, mixins, status, permissions
from django.contrib.auth import get_user_model
from accounts.serializers import (
    UserSerializer)
from utils.permissions import (
    IsSuperUser)


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
    lookup_url_kwarg = 'pk'


    def get_permissions(self):
        # anyone can access the 'create' method
        if self.action == 'create':
            return [permissions.AllowAny()]
        # retrieving all users, and/or a specific user can only be done by a superuser
        elif self.action == 'list' or self.lookup_url_kwarg in self.kwargs:
            return  [IsSuperUser()]
        # actions related to the currently authenticated user
        else:
            return [permissions.IsAuthenticated()]



    def get_object(self):
        # if there's a pk in the url, run the super class's default method
        if self.lookup_url_kwarg in self.kwargs:
            return super().get_object()
        # else, return the currently authenticated user
        else:
            return self.request.user
