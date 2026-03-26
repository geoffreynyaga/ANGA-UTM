from django.urls import include, path, re_path

from . import views
from .auth_views import LoginAPIView, SignupAPIView
from .views import UpdateExpoPushTokenAPIView

urlpatterns = [
    #Auth endpoints
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('push-token/', UpdateExpoPushTokenAPIView.as_view(), name='update_expo_push_token'),

    re_path(
        r"^profile/(?P<pk>\d+)/$",
        views.UserProfileDetailAPIView.as_view(),
        name="userprofile_api",
    ),
    re_path(
        r"^profile/(?P<pk>\d+)/logs/$",
        views.UserProfileFlightLogsListAPIView.as_view(),
        name="userprofile_logs_api",
    ),
    re_path(
        r"^profile/(?P<pk>\d+)/uas/$",
        views.UserProfileUASListAPIView.as_view(),
        name="userprofile_logs_api",
    ),
    # re_path(r"^logs/list/$", views.FlightLogListAPIView.as_view(), name="logs_list_api"),
    # re_path(r"^logs/test/$", views.FlightLogReserveAirspace.as_view(), name="logs_test"),
    # re_path(r'^logs/(?P<pk>\d+)/update$' , views.FlightLogUpdateView.as_view(), name='log_update'),
]
