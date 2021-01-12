from django.conf.urls import url

from djgeojson.views import GeoJSONLayerView

from . import views

urlpatterns = [
        # url(r'^add/$', views.FlightLogCreateView.as_view(), name='logs_add'),

        url(r'^logs/$', views.FlightLogListView.as_view(), name='logs_list'),
        url(r'^logs/(?P<pk>\d+)/$' , views.FlightLogDetailView.as_view(), name='log_detail'),

        url(r'^logs/(?P<pk>\d+)/update$' , views.FlightLogUpdateView.as_view(), name='log_update'),


        url(r'^checklist/$' , views.ChecklistListView.as_view(), name='checklist_list'),
        url(r'^checklist/(?P<pk>\d+)/$' , views.ChecklistDetailView.as_view(), name='checklist_detail'),
        url(r'^checklist/(?P<pk>\d+)/update$' , views.ChecklistUpdateView.as_view(), name='checklist_update'),

        url(r'^emergency-info/add$', views.EmmergencyInfoCreateView.as_view(), name='emergency_add'),
        url(r'^pre-flight/add$', views.PreFlightCreateView.as_view(), name='pre_flight_add'),

        url(r'^postflight/(?P<pk>\d+)/update$' , views.PostFlightUpdateView.as_view(), name='post_flight_update'),
        url(r'^preflight/(?P<pk>\d+)/update$' , views.PreFlightUpdateView.as_view(), name='pre_flight_update'),
        url(r'^emergency-info/(?P<pk>\d+)/update$' , views.EmmergencyInfoUpdateView.as_view(), name='emmergency_info_update'),


        url(r'^notifications/$' , views.unfinished_logs_notifications, name='unfinished_logs_notifications'),

]
