from django.conf.urls import url


from . import views

urlpatterns = [
    url(r"^logs/list/$", views.FlightLogListAPIView.as_view(), name="logs_list"),
    # url(r"^logs/test/$", views.FlightLogReserveAirspace.as_view(), name="logs_test"),
    # url(r'^logs/(?P<pk>\d+)/$' , views.FlightLogDetailView.as_view(), name='log_detail'),
    # url(r'^logs/(?P<pk>\d+)/update$' , views.FlightLogUpdateView.as_view(), name='log_update'),
]

