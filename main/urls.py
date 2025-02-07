from django.urls import re_path
from main.views import (
    EncryptedResourceViewSet,
    EncryptionKeyViewSet,
)
from utils.aliases import *

app_name = 'main'
urlpatterns = [
    re_path('^encrypted-resources/?$', EncryptedResourceViewSet.as_view(LIST_CREATE), name='encrypted-resource-list-create'),
    re_path('^encrypted-resources/(?P<pk>\d+)/?$', EncryptedResourceViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='encrypted-resource-detail'),
    re_path('^encrypted-resources/d/(?P<pk>\d+)/?$', EncryptedResourceViewSet.as_view({'post': 'decrypt_resource'}), name='decrypted-resource-detail'),

    re_path('^encryption-key/?$', EncryptionKeyViewSet.as_view({'post': 'retrieve'})),
]