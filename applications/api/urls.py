from django.urls import include, path, re_path

from applications.api.views import (
    ReserveAirspaceDetailAPIView,
    ReserveAirspaceListAPIView,
    ReserveCreateAPIView,
    ProjectListExtraDetailsAPIView,
    ProjectDetailsAPIView,
)

# from djgeojson.views import GeoJSONLayerView
from applications.models import ReserveAirspace

urlpatterns = [
    path("create/", ReserveCreateAPIView.as_view(), name="create_reserve_api"),
    re_path(
        r"^v1/reserve-airspaces/list/$",
        ReserveAirspaceListAPIView.as_view(),
        name="reserve_airspaces_list_api",
    ),
    re_path(
        r"^v1/reserve-airspaces/(?P<pk>\d+)/$",
        ReserveAirspaceDetailAPIView.as_view(),
        name="reserve_airspace_detail_api",
    ),
    path(
        "v1/projects/list/",
        ProjectListExtraDetailsAPIView.as_view(),
        name="projects_list_api",
    ),
    path(
        "v1/projects/<int:pk>/details/",
        ProjectDetailsAPIView.as_view(),
        name="project_details_api",
    ),
]
