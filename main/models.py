from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from utils.models import TimestampsModel

User = get_user_model()


class EncryptedResource(TimestampsModel):
    """
    An encrypted resource uploaded to the platform.
    """
    uploader = models.ForeignKey(
        User,
        verbose_name = 'resource uploader',
        related_name = 'uploaded_resources',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    file_tag = models.CharField(_('file tag'), max_length=50, null=False, blank=False)
    file_content = models.FileField(_('file content'), upload_to='uploads/', null=False, blank=False)

class ResourceAccess_User(TimestampsModel):
    """
    A resource access rule between a user (grantor) and another user (grantee).
    """
    grantor = models.ForeignKey(
        User,
        verbose_name = 'grantor',
        related_name = 'granted_resources',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    resource = models.ForeignKey(
        EncryptedResource,
        verbose_name = 'resource',
        related_name = 'user_access',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    grantee = models.ForeignKey(
        User,
        verbose_name = 'granted to',
        related_name = 'resource_access',
        on_delete = models.CASCADE,
        null = False,
        blank = False)

class EncryptionKey(TimestampsModel):
    """
    An encryption key that decrypts a particular encrypted resource.
    """
    owner = models.ForeignKey(
        User,
        verbose_name = 'key owner',
        related_name = 'encryption_keys',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    resource = models.ForeignKey(
        EncryptedResource,
        verbose_name = 'resource',
        related_name = 'encryption_keys',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    value = models.CharField(_('key value'), max_length=100, null=False, blank=False)
    usage_count = models.IntegerField(_('usage count'), null=False, blank=False)
    usage_limit = models.IntegerField(_('usage limit'), null=False, blank=False)


# ----- GROUPING MODELS ------ #
class Business(TimestampsModel):
    """
    A higher level model for the User model, representing a business account.
    """
    manager_account = models.ForeignKey(
        User,
        verbose_name = _('manager account'),
        related_name = 'businesses',
        on_delete = models.SET_NULL,
        null = True,
        blank = True)
    name = models.CharField(_('business name'), max_length=100, null=False, blank=False)
    email = models.EmailField(_('business email'), null=False, blank=False)
    def __str__(self):
        return f'{self.name} - {self.email}'


## ORGANISATIONS AND RELATED MODELS
class Organisation(TimestampsModel):
    """
    Higher level container for a business.
    """
    business = models.ForeignKey(
        Business,
        verbose_name = 'parent business',
        related_name = 'organisations',
        on_delete = models.SET_NULL,
        null = True,
        blank = True)
    name = models.CharField(_('organisation name'), max_length=100, null=False, blank=False)
    email = models.EmailField(_('organisation email'), null=False, blank=False)
    address = models.CharField(_('organisation address'), max_length=200, null=True, blank=True)

class OrganisationMember(TimestampsModel):
    """
    A linking model between a User and an Organisation.
    """
    user = models.ForeignKey(
        User,
        verbose_name = 'user account',
        related_name = 'organisation_member_profiles',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    organisation = models.ForeignKey(
        Organisation,
        verbose_name = 'organisation',
        related_name = 'member_profiles',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    organisation_position = models.CharField(max_length = 100, null=True, blank=True)

class ResourceAccess_Organisation(TimestampsModel):
    """
    A resource access rule between a user (grantor) and all other users within an organisation (grantees).
    """
    grantor = models.ForeignKey(
        User,
        verbose_name = 'grantor',
        related_name = 'granted_resources_organisation',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    resource = models.ForeignKey(
        EncryptedResource,
        verbose_name = 'resource',
        related_name = 'organisation_access',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    organisation = models.ForeignKey(
        Organisation,
        verbose_name = 'organisation',
        related_name = 'resource_access',
        on_delete = models.CASCADE,
        null = False,
        blank = False)


## WORKSPACES AND RELATED MODELS
class Workspace(TimestampsModel):
    """
    A department-like construct within an organisation. Comprises of zero or more teams.
    """
    organisation = models.ForeignKey(
        Organisation,
        verbose_name = 'organisation',
        related_name = 'workspaces',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    name = models.CharField(_('workspace name'), max_length=100, null=False, blank=False)

class WorkspaceMember(TimestampsModel):
    """
    A linking model between a User and a Workspace.
    """
    user = models.ForeignKey(
        User,
        verbose_name = 'user account',
        related_name = 'workspace_member_profiles',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    workspace = models.ForeignKey(
        Workspace,
        verbose_name = 'workspace',
        related_name = 'member_profiles',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    workspace_position = models.CharField(max_length = 100, null=True, blank=True)

class ResourceAccess_Workspace(TimestampsModel):
    """
    A resource access rule between a user (grantor) and all other users within a workspace (grantees).
    """
    workspace = models.ForeignKey(
        Workspace,
        verbose_name = 'workspace',
        related_name = 'resource_access',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    resource = models.ForeignKey(
        EncryptedResource,
        verbose_name = 'resource',
        related_name = 'workspace_access',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    grantor = models.ForeignKey(
        User,
        verbose_name = 'grantor',
        related_name = 'granted_resources_workspace',
        on_delete = models.CASCADE,
        null = False,
        blank = False)


## TEAMS AND RELATED MODELS
class Team(TimestampsModel):
    """
    A team within a workspace or department. Comprises of one or more users.
    """
    workspace = models.ForeignKey(
        Workspace,
        verbose_name = 'workspace',
        related_name = 'teams',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    name = models.CharField(_('team name'), max_length=100, null=False, blank=False)

class TeamMember(TimestampsModel):
    """
    A linking model between a User instance and a team.
    """
    user = models.ForeignKey(
        User,
        verbose_name = 'user account',
        related_name = 'team_member_profiles',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    team = models.ForeignKey(
        Team,
        verbose_name = 'team',
        related_name = 'member_profiles',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    team_position = models.CharField(max_length = 100, null=True, blank=True)

class ResourceAccess_Team(TimestampsModel):
    """
    A resource access rule between a user (grantor) and all other members of a team (grantees).
    """
    grantor = models.ForeignKey(
        User,
        verbose_name = 'grantor',
        related_name = 'granted_resources_team',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    resource = models.ForeignKey(
        EncryptedResource,
        verbose_name = 'resource',
        related_name = 'team_access',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
    team = models.ForeignKey(
        Team,
        verbose_name = 'team',
        related_name = 'resource_access',
        on_delete = models.CASCADE,
        null = False,
        blank = False)
