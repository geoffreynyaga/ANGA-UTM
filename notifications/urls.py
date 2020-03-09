from django.conf.urls import url

from . import views

app_name = "notifications"

urlpatterns = [
    url(r"^$", views.NotificationsListView.as_view(), name="notifications_list"),
    url(r"^mark-all$", views.mark_all_notifications_as_read, name="mark_all_as_read"),
    url(
        r"^(?P<pk>\d+)/delete/$",
        views.NotificationDeleteView.as_view(),
        name="notification_delete",
    ),
    url(r"^test$", views.test_notifications, name="test_notification"),
]

