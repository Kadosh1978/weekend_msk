from django.contrib import admin
from .models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("title", "destination", "is_published", "created_at")
    list_filter = ("is_published", "destination")
    search_fields = ("title", "short_description", "content")
    prepopulated_fields = {"slug": ("title",)}
