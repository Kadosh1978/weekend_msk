from django.shortcuts import render
from destinations.models import Destination
from routes.models import Route


def home(request):
    destinations_qs = Destination.objects.filter(is_published=True)

    destinations = destinations_qs.order_by("name")[:6]
    destinations_total = destinations_qs.count()

    latest_routes = (
        Route.objects
        .filter(is_published=True)
        .select_related("destination")
        .order_by("-created_at")[:6]
    )

    return render(
        request,
        "core/home.html",
        {
            "destinations": destinations,
            "destinations_total": destinations_total,
            "latest_routes": latest_routes,
        },
    )