from django.conf.urls import url


from . import views

urlpatterns = [
    url(
        r"^profile/(?P<pk>\d+)/$",
        views.UserProfileDetailAPIView.as_view(),
        name="userprofile_api",
    ),
    url(
        r"^profile/(?P<pk>\d+)/logs/$",
        views.UserProfileFlightLogsListAPIView.as_view(),
        name="userprofile_logs_api",
    ),
    url(
        r"^profile/(?P<pk>\d+)/uas/$",
        views.UserProfileUASListAPIView.as_view(),
        name="userprofile_logs_api",
    ),
    url(r"^login/$", views.LoginAPIView.as_view(), name="login_api"),
    url(r"^signup/$", views.SignUpAPIView.as_view(), name="signup_api"),
    # url(r"^logs/list/$", views.FlightLogListAPIView.as_view(), name="logs_list_api"),
    # url(r"^logs/test/$", views.FlightLogReserveAirspace.as_view(), name="logs_test"),
    # url(r'^logs/(?P<pk>\d+)/update$' , views.FlightLogUpdateView.as_view(), name='log_update'),
]

