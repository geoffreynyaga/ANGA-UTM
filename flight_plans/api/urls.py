from django.urls import include, path, re_path

from . import views

urlpatterns = [
    re_path(
        r"^logs/list/$", views.DailyWorkLogListAPIView.as_view(), name="logs_list_api"
    ),
    re_path(
        r"^v1/checklists/$",
        views.ChecklistTemplateListAPIView.as_view(),
        name="checklist_list_api",
    ),
    re_path(
        r"^v1/checklists/(?P<pk>\d+)/$",
        views.CheckListDetailAPIView.as_view(),
        name="checklist_detail",
    ),
    re_path(
        r"^checklists/add/$",
        views.CheckListTemplateCreateAPIView.as_view(),
        name="checklist_add",
    ),
    path(
        "v1/work-logs/incomplete/list/",
        views.WorkLogListAPIView.as_view(),
        name="work_log_incomplete_list",
    ),
    path(
        "v1/work-logs/add/",
        views.WorkLogCreateAPIView.as_view(),
        name="work_log_add",
    ),
    path(
        "v1/work-logs/<int:pk>/",
        views.WorkLogDetailAPIView.as_view(),
        name="work_log_detail",
    ),
    path(
        "v1/work-logs/<int:pk>/update/",
        views.WorkLogUpdateAPIView.as_view(),
        name="work_log_update",
    ),
    # re_path(r"^logs/test/$", views.FlightLogReserveAirspace.as_view(), name="logs_test"),
    # re_path(r'^logs/(?P<pk>\d+)/update$' , views.FlightLogUpdateView.as_view(), name='log_update'),
]
