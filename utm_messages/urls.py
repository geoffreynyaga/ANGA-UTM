from django.conf.urls import url
from . import views




urlpatterns = [

        url(r'^$', views.InboxListView.as_view(), name='inbox'),
        url(r'^sent/$', views.SentMessagesListView.as_view(), name='sent'),
        url(r'^compose/$', views.MessagesCreateView.as_view(), name='compose'),

        # url(r'^compose-all/$', views.SendToAll.as_view(), name='compose_to_all'),

        url(r'^(?P<pk>\d+)/$', views.MessageDetailView.as_view(), name='message_detail'),

        url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),

        url(r'^notifications/$', views.NotificationsListView.as_view(), name='notifications_list'),

        # url(r'^myreserve/$', views.ReserveAirspaceListView.as_view(), name='my_reserve_list'),
        # url(r'^submissions/datasets$', views.airspace_datasets, name='airspace_datasets'),
        # url(r'update/(?P<pk>\d+)/$' , views.ReserveAirspaceUpdateView.as_view(), name='update_my_airspace'),
        #
        #
        #

]
