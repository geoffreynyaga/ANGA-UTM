from django.conf.urls import url

from .views import (GeofenceLocationsListAPIView, LocationsPointsListAPIView, LocationsPointsCreateAPIView)

urlpatterns = [

    url(r'^$', GeofenceLocationsListAPIView.as_view(), name='geofence_locations_list_api'),

    url(r'^locations/$', LocationsPointsListAPIView.as_view(), name='locations_list_api'),

    url(r'^locations/create/$', LocationsPointsCreateAPIView.as_view(), name='locations_create_api'),

    # url(r'^(?P<pk>\d+)/$', GroupDetailAPIView.as_view(), name='group_detail_api'),
    #
    # url(r'^(?P<pk>\d+)/update/$',
    #     GroupUpdateAPIView.as_view(), name='group_update_api'),
    #
    # url(r'^(?P<pk>\d+)/delete/$',
    #     GroupDeleteAPIView.as_view(), name='group_delete_api'),
    #
    # url(r'^create/$', GroupCreateAPIView.as_view(), name='group_create_api'),
    # url(r'^users/$', GroupCreateUsersListAPIView.as_view(),
    #     name='group_create_users_list_api'),

]
