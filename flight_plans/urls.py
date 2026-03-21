from django.urls import include, path, re_path

from djgeojson.views import GeoJSONLayerView

from . import views

urlpatterns = [
    # re_path(r'^add/$', views.FlightLogCreateView.as_view(), name='logs_add'),
    re_path(r"^logs/$", views.FlightLogListView.as_view(), name="logs_list"),
    re_path(r"^logs/(?P<pk>\d+)/$", views.FlightLogDetailView.as_view(), name="log_detail"),
    re_path(r"^logs/(?P<pk>\d+)/update$", views.FlightLogUpdateView.as_view(), name="log_update"),
    re_path(r"^checklist/$", views.ChecklistListView.as_view(), name="checklist_list"),
    re_path(
        r"^checklist/(?P<pk>\d+)/$", views.ChecklistDetailView.as_view(), name="checklist_detail"
    ),
    re_path(
        r"^checklist/(?P<pk>\d+)/update$",
        views.ChecklistUpdateView.as_view(),
        name="checklist_update",
    ),
    re_path(
        r"^emergency-info/add$", views.EmmergencyInfoCreateView.as_view(), name="emergency_add"
    ),
    re_path(r"^pre-flight/add$", views.PreFlightCreateView.as_view(), name="pre_flight_add"),
    re_path(
        r"^postflight/(?P<pk>\d+)/update$",
        views.PostFlightUpdateView.as_view(),
        name="post_flight_update",
    ),
    re_path(
        r"^preflight/(?P<pk>\d+)/update$",
        views.PreFlightUpdateView.as_view(),
        name="pre_flight_update",
    ),
    re_path(
        r"^emergency-info/(?P<pk>\d+)/update$",
        views.EmmergencyInfoUpdateView.as_view(),
        name="emmergency_info_update",
    ),
    re_path(
        r"^notifications/$",
        views.unfinished_logs_notifications,
        name="unfinished_logs_notifications",
    ),
]
