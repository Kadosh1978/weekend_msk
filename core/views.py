from django.shortcuts import render
from destinations.models import Destination
from routes.models import Route


def home(request):
    destinations = Destination.objects.filter(is_published=True).order_by("name")[:6]
    latest_routes = Route.objects.filter(is_published=True).select_related("destination").order_by("-created_at")[:6]

    return render(
        request,
        "core/home.html",
        {
            "destinations": destinations,
            "latest_routes": latest_routes,
        },
    )