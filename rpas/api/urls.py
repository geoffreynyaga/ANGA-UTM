from django.urls import include, path, re_path

from rpas.api.views import UserRPASListAPIView, UserRPASModelsListAPIView

urlpatterns = [
    re_path(
        r"^v1/my-rpas/list/$",
        UserRPASListAPIView.as_view(),
        name="my_rpas_list_api",
    ),
    path(
        "v1/rpas-models/list/",
        UserRPASModelsListAPIView.as_view(),
        name="rpas_models_list_api",
    ),
    # re_path(
    #     r"^v1/reserve-airspaces/(?P<pk>\d+)/$",
    #     ReserveAirspaceDetailAPIView.as_view(),
    #     name="reserve_airspace_detail_api",
    # ),
]
