from django.urls import include, path, re_path

from . import views

urlpatterns = [
    re_path(r"^logs/list/$", views.FlightLogListAPIView.as_view(), name="logs_list_api"),
    re_path(
        r"^checklists/$",
        views.CheckListAllAPIView.as_view(),
        name="checklist_detail",
    ),
    re_path(
        r"^checklists/(?P<pk>\d+)/$",
        views.CheckListDetailAPIView.as_view(),
        name="checklist_detail",
    ),
    re_path(
        r"^checklists/submit/$",
        views.ChecklistSubmissionCreateAPIView.as_view(),
        name="checklist_submit",
    ),
    # re_path(r"^logs/test/$", views.FlightLogReserveAirspace.as_view(), name="logs_test"),
    # re_path(r'^logs/(?P<pk>\d+)/update$' , views.FlightLogUpdateView.as_view(), name='log_update'),
]
