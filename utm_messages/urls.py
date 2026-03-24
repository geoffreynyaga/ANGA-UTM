from django.urls import include, path, re_path

from . import views

app_name = "messages"

urlpatterns = [
    re_path(r"^$", views.InboxListView.as_view(), name="inbox"),
    re_path(r"^sent/$", views.SentMessagesListView.as_view(), name="sent"),
    re_path(r"^compose/$", views.MessagesCreateView.as_view(), name="compose"),
    # re_path(r'^compose-all/$', views.SendToAll.as_view(), name='compose_to_all'),
    re_path(r"^(?P<pk>\d+)/$", views.MessageDetailView.as_view(), name="message_detail"),
    re_path(r"^calendar/$", views.CalendarView.as_view(), name="calendar"),
]
