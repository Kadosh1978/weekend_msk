from django.urls import path
from .views import destination_detail, destination_list

app_name = "destinations"

urlpatterns = [
    path("", destination_list, name="list"),
    path("<slug:slug>/", destination_detail, name="detail"),
]