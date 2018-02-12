from django.conf.urls import url
from . import views

from djgeojson.views import GeoJSONLayerView
from .models import ReserveAirspace

urlpatterns = [
        # url(r'^$', views.ReserveAirspaceCreateView.as_view(), name='create_reserve'),
        url(r'^$', views.ReserveAirspaceMainView.as_view(), name='reserve_main'),

        url(r'^create/$', views.ReserveAirspaceCreateView.as_view(), name='create_reserve'),
        url(r'^airspace/$', views.view_airspace, name='view_airspace'),

        url(r'^myreserve/$', views.ReserveAirspaceListView.as_view(), name='my_reserve_list'),
        url(r'^myreserve/datasets$', views.my_reserve_datasets, name='my_reserve_datasets'),

        url(r'^submissions/datasets$', GeoJSONLayerView.as_view(model=ReserveAirspace,
        properties=('start_time','start_day','end','status','get_name','get_rpas',
                    'get_organization','get_rpas_pic','get_start_day','get_phone_number','created_by')),
        name='airspace_datasets'),
        # url(r'^submissions/datasets$', views.airspace_datasets, name='airspace_datasets'),
        url(r'update/(?P<pk>\d+)/$' , views.ReserveAirspaceUpdateView.as_view(), name='update_my_airspace'),


        url(r'^myreserve/(?P<pk>\d+)/$' , views.ReserveAirspaceDetailView.as_view(), name='myreserve_detail'),

        url(r'^approval-letters/$', views.MyApprovalLettersListView.as_view(), name='my_approval_letters_list'),
        url(r'^approval-letters/(?P<pk>\d+)/$' , views.MyApprovalLettersDetailView.as_view(), name='my_approval_letters_detail'),


        url(r'^applied-reserves/$', views.AppliedReserveAirspaceListView.as_view(), name='applied_reserves'),
        url(r'^applied-reserves/(?P<pk>\d+)/$' , views.AppliedReserveAirspaceDetailView.as_view(), name='applied_reserves_detail'),
        url(r'^applied-reserves/(?P<pk>\d+)/update/$' , views.AppliedReserveAirspaceUpdateView.as_view(), name='applied_reserves_update'),

        # url(r'update/(?P<pk>\d+)/$' , views.FlightLogUpdateView.as_view(), name='log_update'),
        #
        # url(r'^locations/$', views.locations_datasets, name='locations'),
        # url(r'^time/$', views.view_time.as_view(), name='view_time'),
        # url(r'^time/add$', views.TimeCreateView.as_view(), name='add_time'),


        #
        # url(r'^missionpath/add$', views.MissionPathCreateView.as_view(), name='path_add'),
        url(r'^applications/mydata/(?P<pk>\d+)/$', views.my_airspace_datasets, name='my_airspace_datasets'),
        # url(r'^missionlist/view/$', views.MissionPathListView.as_view(), name='path'),
        # url(r'^missionlist/(?P<pk>\d+)/$', views.MissionPathDetailView.as_view(), name='path_detail'),


        # url(r'^missionobjective/add$', views.MissionObjectiveCreateView.as_view(), name='objective_add'),
        # url(r'^missionlocation/add$', views.MissionLocationCreateView.as_view(), name='location_add'),
        # url(r'^emergency-info/add$', views.EmmergencyInfoCreateView.as_view(), name='emergency_add'),
        # url(r'^pre-flight/add$', views.PreFlightCreateView.as_view(), name='pre_flight_add'),

        url(r'^logs/create/$', views.LogsUploadCreateView.as_view(), name='create_log_upload'),
        url(r'^logs/$', views.LogsUploadListView.as_view(), name='log_list_geom'),


]
