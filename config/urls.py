from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("destinations/", include("destinations.urls")),
    path("routes/", include("routes.urls")),
]
