from django.conf.urls import url

from . import views

app_name = "messages"

urlpatterns = [

        url(r'^$', views.InboxListView.as_view(), name='inbox'),
        url(r'^sent/$', views.SentMessagesListView.as_view(), name='sent'),
        url(r'^compose/$', views.MessagesCreateView.as_view(), name='compose'),

        # url(r'^compose-all/$', views.SendToAll.as_view(), name='compose_to_all'),

        url(r'^(?P<pk>\d+)/$', views.MessageDetailView.as_view(), name='message_detail'),

        url(r'^calendar/$', views.CalendarView.as_view(), name='calendar'),

        ]
