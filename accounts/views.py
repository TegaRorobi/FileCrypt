from rest_framework import viewsets, mixins, status, permissions
from rest_framework.response import Response
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


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_businesses = instance.businesses.all()

        if user_businesses:
            # business.notify_members_about_deletion()
            # start a timer, and delete the business in 7 days.
            # there should also be a way to stop the deletion.
            return Response({
                'message': 'User account is tied to one or more businesses.'
                           'Members associated with this business will be notified.'
                           'Business deletion will take place in 7 days.'
            }, status=status.HTTP_202_ACCEPTED)
        else:
            instance.delete()
            return Response({'message': 'User account successfully deleted.'}, status=status.HTTP_204_NO_CONTENT)
