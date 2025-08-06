from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from jobs.urls import router as jobs_router

if settings.DEBUG:
    router = routers.DefaultRouter()
else:
    router = routers.SimpleRouter()

router.registry.extend(jobs_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("", include("jobs.urls")),
]
