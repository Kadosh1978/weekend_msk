from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "transport_type", "is_published", "created_at")
    list_filter = ("is_published", "transport_type")
    search_fields = (
        "name",
        "short_description",
        "description",
        "how_to_get",
        "what_to_see",
        "budget",
        "days_count",
    )
    prepopulated_fields = {"slug": ("name",)}