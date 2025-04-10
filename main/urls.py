from django.urls import re_path
from main.views import (
    EncryptedResourceViewSet,
    EncryptionKeyViewSet,
    BusinessViewSet,
    OrganisationViewSet,
    WorkspaceViewSet,
    TeamViewSet
)
from utils.aliases import *

app_name = 'main'

encryption_endpoints = [
    re_path('^encrypted-resources/?$', EncryptedResourceViewSet.as_view(LIST_CREATE), name='encrypted-resource-list-create'),
    re_path('^encrypted-resources/(?P<pk>\d+)/?$', EncryptedResourceViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='encrypted-resource-detail'),
    re_path('^encrypted-resources/d/(?P<pk>\d+)/?$', EncryptedResourceViewSet.as_view({'post': 'decrypt_resource'}), name='decrypted-resource-detail'),

    re_path('^encryption-key/?$', EncryptionKeyViewSet.as_view({'post': 'retrieve'})),
]



business_endpoints = [
    # A SuperUser or regular user creating a business account, of which they would be the manager.
    re_path('businesses/create/?$', BusinessViewSet.as_view(CREATE), name='businesses-create'),

    # A SuperUser listing out, retrieving or deleting business accounts.
    re_path('businesses/?$', BusinessViewSet.as_view(LIST), name='businesses-list'),
    re_path('businesses/(?P<pk>\d+)/?$', BusinessViewSet.as_view(RETRIEVE_DESTROY), name='business-detail'),

    # A business manager effecting changes within the business(es) they manage.
    re_path('businesses/me/managed/?$', BusinessViewSet.as_view(LIST), name='businesses-list-managed'),
    re_path('businesses/me/managed/(?P<pk>\d+)/?$', BusinessViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='business-detail-managed'),

    # A team member getting information about the business(es) they're a part of, with information
    # of the organisations, workspaces, teams, down to the team member profiles which represent their user account.
    re_path('businesses/me/?$', BusinessViewSet.as_view(LIST), name='businesses-list-me'),
    re_path('businesses/me/(?P<pk>\d+)/?$', BusinessViewSet.as_view(RETRIEVE), name='business-detail-me'),
]



organisation_endpoints = [
    # A SuperUser or regular user creating an organisation account.
    re_path('organisations/create/?$', OrganisationViewSet.as_view(CREATE), name='organisations-create'),

    # A SuperUser listing, retrieving or deleting an organisation account.
    re_path('organisations/?$', OrganisationViewSet.as_view(LIST), name='organisations-list'),
    re_path('organisations/(?P<pk>\d+)/?$', OrganisationViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='organisation-detail'),

    # A team member getting information about the organisation(s) they're a part of, with information
    # of the workspaces, teams, down to the team member profiles which represent their user account.
    re_path('organisations/me/?$', OrganisationViewSet.as_view(LIST), name='organisations-list-me'),
    re_path('organisations/me/(?P<pk>\d+)/?$', OrganisationViewSet.as_view(RETRIEVE), name='organisation-detail-me'),
]



workspace_endpoints = [
    # A SuperUser or regular user creating a workspace account.
    re_path('workspaces/create/?$', WorkspaceViewSet.as_view(CREATE), name='workspaces-create'),

    # A SuperUser listing out, retrieving or deleting a workspace account.
    re_path('workspaces/?$', WorkspaceViewSet.as_view(LIST), name='workspaces-list'),
    re_path('workspaces/(?P<pk>\d+)/?$', WorkspaceViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='workspace-detail'),

    # A team member getting information about the workspace(s) they're a part of, with information
    # of the teams, down to the team member profiles which represent their user account.
    re_path('workspaces/me/?$', WorkspaceViewSet.as_view(LIST), name='workspaces-list-me'),
    re_path('workspaces/me/(?P<pk>\d+)/?$', WorkspaceViewSet.as_view(RETRIEVE), name='workspace-detail-me'),
]



team_endpoints = [
    # A SuperUser or regular user creating an team account.
    re_path('teams/create/?$', TeamViewSet.as_view(CREATE), name='teams-create'),

    # A SuperUser listing out or retrieving or deleting a team account.
    re_path('teams/?$', TeamViewSet.as_view(LIST), name='teams-list'),
    re_path('teams/(?P<pk>\d+)/?$', TeamViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='team-detail'),

    # A team member getting information about the team(s) they're a part of, with information
    # of the team member profiles which represent their user account.
    re_path('teams/me/?$', TeamViewSet.as_view(LIST), name='teams-list-me'),
    re_path('teames/me/(?P<pk>\d+)/?$', TeamViewSet.as_view(RETRIEVE), name='team-detail-me'),
]


urlpatterns = [
    *encryption_endpoints,
    *business_endpoints,
    *organisation_endpoints,
    *workspace_endpoints,
    *team_endpoints
]