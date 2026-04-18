from django.shortcuts import get_object_or_404, render
from .models import Destination


def destination_detail(request, slug):
    destination = get_object_or_404(
        Destination,
        slug=slug,
        is_published=True,
    )
    return render(
        request,
        "destinations/detail.html",
        {"destination": destination},
    )