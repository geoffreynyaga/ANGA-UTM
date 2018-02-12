from django.conf.urls import url
from . import views

from djgeojson.views import GeoJSONLayerView

urlpatterns = [
        url(r'logs/add$', views.FlightLogCreateView.as_view(), name='logs_add'),

        url(r'^logs/$', views.FlightLogListView.as_view(), name='logs_list'),
        url(r'^logs/(?P<pk>\d+)/$' , views.FlightLogDetailView.as_view(), name='log_detail'),

        url(r'update/(?P<pk>\d+)/$' , views.FlightLogUpdateView.as_view(), name='log_update'),


        url(r'^missionpath/add$', views.MissionPathCreateView.as_view(), name='path_add'),
        url(r'^missionlist/data/(?P<pk>\d+)/$', views.path_datasets, name='path_dataset'),
        url(r'^missionlist/view/$', views.MissionPathListView.as_view(), name='path'),
        url(r'^missionlist/(?P<pk>\d+)/$', views.MissionPathDetailView.as_view(), name='path_detail'),

        url(r'^checklist/$' , views.ChecklistListView.as_view(), name='checklist_list'),
        url(r'^checklist/(?P<pk>\d+)/$' , views.ChecklistDetailView.as_view(), name='checklist_detail'),
        url(r'^checklist/(?P<pk>\d+)/update$' , views.ChecklistUpdateView.as_view(), name='checklist_update'),


        url(r'^missionobjective/add$', views.MissionObjectiveCreateView.as_view(), name='objective_add'),
        url(r'^missionlocation/add$', views.MissionLocationCreateView.as_view(), name='location_add'),
        url(r'^emergency-info/add$', views.EmmergencyInfoCreateView.as_view(), name='emergency_add'),
        url(r'^pre-flight/add$', views.PreFlightCreateView.as_view(), name='pre_flight_add'),


]
