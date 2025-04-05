from rest_framework import (
    viewsets, mixins, permissions, status, decorators
)
from rest_framework.response import Response
from django.db.models import QuerySet, Prefetch
from django.urls import resolve
from django.http import FileResponse
from django.shortcuts import get_object_or_404

from main.models import (
    EncryptedResource,
    EncryptionKey,
    Business,
    Organisation,
    Workspace,
    Team,
    TeamMember)
from main.serializers import (
    EncryptedResourceSerializer,
    EncryptedResourceCreateSerializer,
    EncryptionKeyForDecryptingResourceSerializer,
    EncryptionKeySerializer,
    BusinessSerializer,
    OrganisationSerializer,
    WorkspaceSerializer,
    TeamSerializer)
from main.serializers2 import (
    BusinessSerializer2,
    OrganisationSerializer2,
    WorkspaceSerializer2,
    TeamSerializer2
)
from utils.permissions import (
    NotAllowed,
    IsSuperUser,
    IsOrganisationAdminOrSuperUser,
    IsOrganisationMemberOrSuperUser)
from utils.crypt import EncryptionManager
from cryptography.fernet import InvalidToken



class EncryptedResourceViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):

    # parser_classes = [parsers.FileUploadParser]

    def get_permissions(self):
        if self.action == 'decrypt_resource':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'decrypt_resource':
            return EncryptionKeyForDecryptingResourceSerializer
        if self.action == 'create':
            return EncryptedResourceCreateSerializer
        return EncryptedResourceSerializer

    def get_queryset(self):
        return self.request.user.uploaded_resources.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(uploader=self.request.user)
        encryption_key = instance.encryption_keys.get()
        headers = self.get_success_headers(serializer.data)
        return Response({
            **serializer.data,
            'encryption_key':encryption_key.value
        }, status=status.HTTP_201_CREATED, headers=headers)

    @decorators.action(detail=True)
    def decrypt_resource(self, request, *args, **kwargs):
        resource = self.get_object()
        encryption_key_value = request.data['encryption_key']

        try:
            decrypted_resource_url, decrypted_file_path, decrypted_data = EncryptionManager().decrypt_file(
                input_file=resource.file_content,
                encryption_key=encryption_key_value,
                http_origin=request.META.get('HTTP_ORIGIN')
            )

            # Usage tracking on an encryption key.
            encryption_key = EncryptionKey.objects.get(value=encryption_key_value)

            encryption_key.usage_count += 1
            if encryption_key.usage_count > encryption_key.usage_limit:
                return Response({'message': 'Encryption Key Expired.'}, status=status.HTTP_400_BAD_REQUEST)
            encryption_key.save()

        except InvalidToken or EncryptionKey.DoesNotExist:
            return Response({'message': 'Invalid Encryption key for this resource.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'url': decrypted_resource_url}, status=status.HTTP_200_OK)


class EncryptionKeyViewSet(viewsets.GenericViewSet):

    serializer_class = EncryptionKeySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return EncryptionKey.objects.get(owner=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        resource_id = request.data['resource_id']
        try:
            resource = EncryptedResource.objects.get(id=resource_id)
        except:
            return Response({'message': 'Resource not found.'}, status=status.HTTP_404_NOT_FOUND)
        encryption_key = resource.encryption_keys.get()
        serializer = self.get_serializer(encryption_key)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BusinessViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):

    def get_serializer_class(self):
        url_name = resolve(self.request.path_info).url_name
        if url_name in ['businesses-list-me']:
            return BusinessSerializer2
        return BusinessSerializer

    def get_queryset(self):
        url_name = resolve(self.request.path_info).url_name
        if url_name in ['businesses-list', 'business-detail']:
            if self.request.user.is_superuser:
                return Business.objects.all()

        elif url_name in ['businesses-list-managed', 'business-detail-managed']:
            return self.request.user.businesses.all()

        elif url_name in ['businesses-list-me', 'business-detail-me']:
            return Business.objects.filter(
                organisations__workspaces__teams__member_profiles__user=self.request.user
            ).distinct().prefetch_related(
                Prefetch('organisations', queryset=Organisation.objects.all()),
                Prefetch('organisations__workspaces', queryset=Workspace.objects.all()),
                Prefetch('organisations__workspaces__teams', queryset=Team.objects.all()),
                Prefetch('organisations__workspaces__teams__member_profiles', queryset=TeamMember.objects.all())
            )

        return QuerySet()

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(manager_account=self.request.user)

    """
    If the manager account of a business is changed, there should be a countdown to the
    transfer (about 3 days), and all users associated with the business should be notified of this change.

    A notification also gets sent out when other fields are updated, but there's no countdown.

    Smells like celery.
    """
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class OrganisationViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):

    def get_serializer_class(self):
        url_name = resolve(self.request.path_info).url_name
        if url_name in ['organisations-list-me', 'organisation-detail-me']:
            return OrganisationSerializer2
        return OrganisationSerializer

    def get_queryset(self):
        url_name = resolve(self.request.path_info).url_name
        if url_name in ['organisations-list', 'organisation-detail']:
            if self.request.user.is_superuser:
                return Organisation.objects.all()

        elif url_name in ['organisations-list-me', 'organisation-detail-me']:
            return Organisation.objects.filter(
                workspaces__teams__member_profiles__user=self.request.user
            ).distinct().prefetch_related(
                Prefetch('workspaces', queryset=Workspace.objects.all()),
                Prefetch('workspaces__teams', queryset=Team.objects.all()),
                Prefetch('workspaces__teams__member_profiles', queryset=TeamMember.objects.all())
            )

        return QuerySet()

    def get_permissions(self):
        return [permissions.IsAuthenticated()]


class WorkspaceViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin):

    def get_serializer_class(self):
        url_name = resolve(self.request.path_info).url_name
        if url_name in ['workspaces-list-me', 'workspace-detail-me']:
            return WorkspaceSerializer2
        return WorkspaceSerializer

    def get_queryset(self):
        url_name = resolve(self.request.path_info).url_name
        if url_name in ['workspaces-list', 'workspace-detail']:
            if self.request.user.is_superuser:
                return Workspace.objects.all()

        elif url_name in ['workspaces-list-me', 'workspace-detail-me']:
            return Workspace.objects.filter(
                teams__member_profiles__user=self.request.user
            ).distinct().prefetch_related(
                Prefetch('teams', queryset=Team.objects.all()),
                Prefetch('teams__member_profiles', queryset=TeamMember.objects.all())
            )

        return QuerySet()

    def get_permissions(self):
        return [permissions.IsAuthenticated()]


