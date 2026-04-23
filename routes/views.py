from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from .models import Route


def route_list(request):
    routes_queryset = (
        Route.objects
        .filter(is_published=True)
        .select_related("destination")
        .order_by("-created_at")
    )

    paginator = Paginator(routes_queryset, 6)
    page_number = request.GET.get("page")
    routes = paginator.get_page(page_number)

    return render(
        request,
        "routes/list.html",
        {"routes": routes},
    )


def route_detail(request, slug):
    route = get_object_or_404(
        Route.objects.select_related("destination"),
        slug=slug,
        is_published=True,
    )
    return render(request, "routes/detail.html", {"route": route})