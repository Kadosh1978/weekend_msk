from django.urls import path
from .views import route_detail, route_list

app_name = "routes"

urlpatterns = [
    path("", route_list, name="list"),
    path("<slug:slug>/", route_detail, name="detail"),
]