from django.shortcuts import get_object_or_404, render
from .models import Destination


def destination_list(request):
    destinations = (
        Destination.objects
        .filter(is_published=True)
        .order_by("name")
    )

    return render(
        request,
        "destinations/list.html",
        {"destinations": destinations},
    )


def destination_detail(request, slug):
    destination = get_object_or_404(
        Destination,
        slug=slug,
        is_published=True,
    )
    routes = destination.routes.filter(is_published=True)

    return render(
        request,
        "destinations/detail.html",
        {
            "destination": destination,
            "routes": routes,
        },
    )