from django.conf.urls import url


from rpas.api.views import UserRPASListAPIView

urlpatterns = [
    url(r"^v1/my-rpas/list/$", UserRPASListAPIView.as_view(), name="my_rpas_list_api",),
    # url(
    #     r"^v1/reserve-airspaces/(?P<pk>\d+)/$",
    #     ReserveAirspaceDetailAPIView.as_view(),
    #     name="reserve_airspace_detail_api",
    # ),
]
