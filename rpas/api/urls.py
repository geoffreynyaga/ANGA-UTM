from django.urls import include, path, re_path

from rpas.api.views import UserRPASListAPIView

urlpatterns = [
    re_path(
        r"^v1/my-rpas/list/$",
        UserRPASListAPIView.as_view(),
        name="my_rpas_list_api",
    ),
    # re_path(
    #     r"^v1/reserve-airspaces/(?P<pk>\d+)/$",
    #     ReserveAirspaceDetailAPIView.as_view(),
    #     name="reserve_airspace_detail_api",
    # ),
]
