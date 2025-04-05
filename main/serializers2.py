from rest_framework import serializers
from django.contrib.auth import get_user_model
from main.models import (
    Business,
    Organisation,
    Workspace,
    Team)
from accounts.serializers import UserSerializer


User = get_user_model()



class TeamSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class WorkspaceSerializer2(serializers.ModelSerializer):
    teams = TeamSerializer2(many=True, required=False, read_only=True)
    class Meta:
        model = Workspace
        fields = '__all__'

class OrganisationSerializer2(serializers.ModelSerializer):
    workspaces = WorkspaceSerializer2(many=True, required=False, read_only=True)
    class Meta:
        model = Organisation
        fields = '__all__'

class BusinessSerializer2(serializers.ModelSerializer):
    manager_account = UserSerializer(required=False, read_only=True)
    organisations = OrganisationSerializer2(many=True, required=False, read_only=True)
    class Meta:
        model = Business
        fields = '__all__'
