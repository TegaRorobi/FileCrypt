from django.urls import re_path
from accounts.views import *
from utils.aliases import *

urlpatterns = [
    re_path('^users/?$', UsersViewSet.as_view(LIST_CREATE), name='users-list-create'),
    re_path('^users/(?P<pk>\d+)/?$', UsersViewSet.as_view(RETRIEVE_UPDATE_DESTROY), name='user-detail'),
]