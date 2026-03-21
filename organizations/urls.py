from django.urls import include, path, re_path

from . import views

urlpatterns = [
    re_path(
        r"^logs/$", views.AllCompanyFlightLogs.as_view(), name="all_company_flight_logs"
    ),
    # re_path(r'^compose-all/$', views.SendToAll.as_view(), name='compose_to_all'),
    # re_path(r'^(?P<pk>\d+)/$', views.MessageDetailView.as_view(), name='message_detail'),
    # re_path(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),
    # re_path(r'^notifications/$', views.NotificationsListView.as_view(), name='notifications_list'),
]
