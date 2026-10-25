from django.urls import path

from maintenance.api import views

urlpatterns = [
    path(
        "v1/records/",
        views.MaintenanceRecordListCreateAPIView.as_view(),
        name="maintenance_records_api",
    ),
    path(
        "v1/records/<int:pk>/",
        views.MaintenanceRecordDetailAPIView.as_view(),
        name="maintenance_record_detail_api",
    ),
    path("v1/rpas/", views.MaintenanceRpasListAPIView.as_view(), name="maintenance_rpas_api"),
    path(
        "v1/installable-requests/",
        views.InstallableRequestListAPIView.as_view(),
        name="maintenance_installable_requests_api",
    ),
    path(
        "v1/report-template/",
        views.ReportTemplateAPIView.as_view(),
        name="maintenance_report_template_api",
    ),
]
