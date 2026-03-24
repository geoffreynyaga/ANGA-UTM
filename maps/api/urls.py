from django.urls import include, path, re_path

from .views import (
    GeofenceLocationsListAPIView,
    LocationsPointsCreateAPIView,
    LocationsPointsListAPIView,
    ObstaclesListAPIView,
    all_airports_datasets,
)

urlpatterns = [
    re_path(
        r"^geofence-locations/$",
        GeofenceLocationsListAPIView.as_view(),
        name="geofence_locations_list_api",
    ),
    re_path(
        r"^locations/$", LocationsPointsListAPIView.as_view(), name="locations_list_api"
    ),
    re_path(
        r"^locations/create/$",
        LocationsPointsCreateAPIView.as_view(),
        name="locations_create_api",
    ),
    re_path(r"^obstacles/$", ObstaclesListAPIView.as_view(), name="obstacles_list_api"),
    path(
        "airports/list/",
        all_airports_datasets,
        name="airports_datasets_api",
    ),
    # re_path(r'^(?P<pk>\d+)/$', GroupDetailAPIView.as_view(), name='group_detail_api'),
    #
    # re_path(r'^(?P<pk>\d+)/update/$',
    #     GroupUpdateAPIView.as_view(), name='group_update_api'),
    #
    # re_path(r'^(?P<pk>\d+)/delete/$',
    #     GroupDeleteAPIView.as_view(), name='group_delete_api'),
    #
    # re_path(r'^create/$', GroupCreateAPIView.as_view(), name='group_create_api'),
    # re_path(r'^users/$', GroupCreateUsersListAPIView.as_view(),
    #     name='group_create_users_list_api'),
]
