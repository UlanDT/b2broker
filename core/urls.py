"""Module containing project urls."""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Allur workspace API",
        default_version="v1",
    ),
    permission_classes=[
        permissions.AllowAny,
    ],
    public=True,
)

urlpatterns = [
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger"),
    path("admin/", admin.site.urls),
    path("api/", include("core.api")),
]
