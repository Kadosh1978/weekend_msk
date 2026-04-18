from django.shortcuts import render
from destinations.models import Destination


def home(request):
    destinations = Destination.objects.filter(is_published=True)[:6]
    return render(request, "core/home.html", {"destinations": destinations})