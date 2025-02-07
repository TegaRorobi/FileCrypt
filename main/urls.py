from django.urls import re_path
from main.views import (
    EncryptedResourceViewSet,
    EncryptionKeyViewSet,
    BusinessViewSet,
)
from utils.aliases import *

app_name = 'main'
urlpatterns = [
    re_path('^encrypted-resources/?$', EncryptedResourceViewSet.as_view(LIST_CREATE), name='encrypted-resource-list-create'),
    re_path('^encrypted-resources/(?P<pk>\d+)/?$', EncryptedResourceViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='encrypted-resource-detail'),
    re_path('^encrypted-resources/d/(?P<pk>\d+)/?$', EncryptedResourceViewSet.as_view({'post': 'decrypt_resource'}), name='decrypted-resource-detail'),

    re_path('^encryption-key/?$', EncryptionKeyViewSet.as_view({'post': 'retrieve'})),

    re_path('businesses/list/?$', BusinessViewSet.as_view(LIST), name='businesses-list'),
    re_path('businesses/?$', BusinessViewSet.as_view(CREATE), name='businesses-create'),
    re_path('businesses/me/?$', BusinessViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='businesses-detail-me'),
    re_path('businesses/(?P<pk>\d+)/?$', BusinessViewSet.as_view(RETRIEVE_DESTROY), name='business-detail'),
]