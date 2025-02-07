"""
URL configuration for filecrypt project.
"""

from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    info = openapi.Info(
        title="FileCrypt API",
        default_version='v1',
        description="FileCrypt API Documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@django.site"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes = (AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),

    # rest_framework (mainly auth)
    path('', include('rest_framework.urls')),

    # swagger/redoc
    re_path('^api/swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(), name='schema-json'),
    re_path('^api/swagger/?$', schema_view.with_ui('swagger'), name='schema-swagger'),
    re_path('^api/redoc/?$', schema_view.with_ui('redoc'), name='schema-redoc'),

    # media/static
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
]
