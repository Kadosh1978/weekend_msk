from django.contrib import admin

from .models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "destination",
        "estimated_time",
        "is_published",
        "created_at",
    )
    list_filter = (
        "destination",
        "is_published",
        "created_at",
    )
    search_fields = (
        "title",
        "slug",
        "short_description",
        "content",
    )
    prepopulated_fields = {
        "slug": ("title",),
    }
    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "destination",
                    "title",
                    "slug",
                    "short_description",
                    "estimated_time",
                    "is_published",
                )
            },
        ),
        (
            "Описание маршрута",
            {
                "fields": (
                    "route_includes",
                    "suitable_for",
                    "content",
                )
            },
        ),
        (
            "Фотографии маршрута",
            {
                "fields": (
                    "route_image_1",
                    "route_image_1_caption",
                    "route_image_2",
                    "route_image_2_caption",
                    "route_image_3",
                    "route_image_3_caption",
                )
            },
        ),
        (
            "Служебное",
            {
                "fields": (
                    "created_at",
                )
            },
        ),
    )
