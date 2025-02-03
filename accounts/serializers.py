from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only':True},
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only':True},
            'user_permissions': {'read_only':True},
            'user_groups': {'read_only':True},
            'created_at': {'read_only':True},
            'updated_at': {'read_only':True},
            'last_login': {'read_only':True},
        }

    def create(self, validated_data):
        clear_password = validated_data['password']
        validated_data['password'] = make_password(clear_password)
        validated_data.setdefault('is_active', True)
        validated_data.setdefault('is_superuser', False)
        validated_data.setdefault('is_staff', False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            clear_password = validated_data['password']
            validated_data['password'] = make_password(clear_password)
        return super().update(instance, validated_data)