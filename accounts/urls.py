from django.urls import re_path
from accounts.views import *
from utils.aliases import *

from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_refresh,
    token_blacklist)


urlpatterns = [
    re_path('^auth/login/?$', token_obtain_pair, name='api-login'),
    re_path('^auth/login/refresh/?$', token_refresh, name='api-login-refresh'),
    re_path('^auth/logout/?$', token_blacklist, name='api-logout'),

    re_path('^users/?$', UsersViewSet.as_view(LIST_CREATE), name='users-list-create'),
    re_path('^users/me/?$', UsersViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='user-detail-me'),
    re_path('^users/(?P<pk>\d+)/?$', UsersViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='user-detail'),
]