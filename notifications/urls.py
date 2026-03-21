from django.urls import include, path, re_path

from . import views

app_name = "notifications"

urlpatterns = [
    re_path(r"^$", views.NotificationsListView.as_view(), name="notifications_list"),
    re_path(r"^mark-all$", views.mark_all_notifications_as_read, name="mark_all_as_read"),
    re_path(
        r"^(?P<pk>\d+)/delete/$",
        views.NotificationDeleteView.as_view(),
        name="notification_delete",
    ),
    re_path(r"^test$", views.test_notifications, name="test_notification"),
]
