from django.conf.urls import url


from . import views

urlpatterns = [
    url(r"^logs/list/$", views.FlightLogListAPIView.as_view(), name="logs_list_api"),
    url(
        r"^checklists/$", views.CheckListAllAPIView.as_view(), name="checklist_detail",
    ),
    url(
        r"^checklists/(?P<pk>\d+)/$",
        views.CheckListDetailAPIView.as_view(),
        name="checklist_detail",
    ),
    # url(r"^logs/test/$", views.FlightLogReserveAirspace.as_view(), name="logs_test"),
    # url(r'^logs/(?P<pk>\d+)/update$' , views.FlightLogUpdateView.as_view(), name='log_update'),
]

