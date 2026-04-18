from django.urls import path
from .views import destination_detail

app_name = "destinations"

urlpatterns = [
    path("<slug:slug>/", destination_detail, name="detail"),
]