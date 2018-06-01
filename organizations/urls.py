from django.conf.urls import url

from . import views

urlpatterns = [

        url(r'^logs/$', views.AllCompanyFlightLogs.as_view(), name='all_company_flight_logs'),

        url(r'^postholder/create/$', views.PostHolderCreateView.as_view(), name='postholder_create'),

        # url(r'^compose-all/$', views.SendToAll.as_view(), name='compose_to_all'),

        # url(r'^(?P<pk>\d+)/$', views.MessageDetailView.as_view(), name='message_detail'),

        # url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),

        # url(r'^notifications/$', views.NotificationsListView.as_view(), name='notifications_list'),

        ]
