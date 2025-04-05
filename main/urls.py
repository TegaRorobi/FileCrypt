from django.urls import re_path
from main.views import (
    EncryptedResourceViewSet,
    EncryptionKeyViewSet,
    BusinessViewSet,
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


urlpatterns = [
    *encryption_endpoints,
    *business_endpoints,
]