from rest_framework import serializers
from django.contrib.auth import get_user_model
from main.models import (
    EncryptedResource,
    EncryptionKey,
    Business,
    Organisation,
    Workspace,
    Team)
from accounts.serializers import UserSerializer
from utils.crypt import EncryptionManager


User = get_user_model()

class EncryptedResourceSerializer(serializers.ModelSerializer):
    uploader_ = UserSerializer(source='uploader', required=False, read_only=True)
    class Meta:
        model = EncryptedResource
        fields = '__all__'
        extra_kwargs = {
            'uploader': {'read_only': True},
            'uploader_': {'read_only': True},
            'file_content': {'read_only': True},
        }

    def create(self, validated_data):
        clear_file = validated_data['file_content']
        encrypted_file, encryption_key_value = EncryptionManager().encrypt_file(input_file=clear_file)
        validated_data['file_content'] = encrypted_file
        instance = super().create(validated_data)

        EncryptionKey.objects.create(
            owner=validated_data['uploader'],
            resource=instance,
            value=encryption_key_value,
            usage_count=0,
            usage_limit=10
        )
        return instance


class EncryptedResourceCreateSerializer(EncryptedResourceSerializer):
    class Meta(EncryptedResourceSerializer.Meta):
        extra_kwargs = {
            **EncryptedResourceSerializer.Meta.extra_kwargs,
            'file_content': {'read_only': False},
        }


class EncryptionKeyForDecryptingResourceSerializer(serializers.Serializer):
    encryption_key = serializers.CharField(required=False)


class EncryptionKeySerializer(serializers.ModelSerializer):
    resource_id = serializers.IntegerField(required=True, write_only=True)
    class Meta:
        model = EncryptionKey
        fields = '__all__'
        extra_kwargs = {
            'owner': {'read_only': True},
            'resource': {'read_only': True},
            'value': {'read_only': True},
            'usage_count': {'read_only': True},
            'usage_limit': {'read_only': True},
        }


class BusinessSerializer(serializers.ModelSerializer):
    manager_account_ = UserSerializer(source='manager_account', required=False, read_only=True)
    class Meta:
        model = Business
        fields = '__all__'
        extra_kwargs = {
            'manager_account_': {'read_only': True},
        }


class OrganisationSerializer(serializers.ModelSerializer):
    business_ = BusinessSerializer(source='business', required=False, read_only=True)
    class Meta:
        model = Organisation
        fields = '__all__'
        extra_kwargs = {
            'business_': {'read_only': True},
        }

        