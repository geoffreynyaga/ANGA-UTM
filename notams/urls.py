from django.urls import include, path, re_path

from . import views
from .models import NotamAirspace

urlpatterns = [
    re_path(
        r"^airspace/datasets/$",
        views.NotamLayer.as_view(
            model=NotamAirspace,
            properties=(
                "notam_number",
                "get_start_day",
                "start_time",
                "end",
                "reason",
                "get_file_url",
            ),
        ),
        name="notam_datasets",
    ),
    re_path(r"^create/$", views.NotamCreateView.as_view(), name="create_notam"),
]
