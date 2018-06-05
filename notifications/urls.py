from django.conf.urls import url

from . import views

urlpatterns = [

        url(r'^$', views.NotificationsListView.as_view(), name='notifications_list'),
        url(r'^mark-all$', views.mark_all_notifications_as_read, name='mark_all_as_read'),
        url(r'^(?P<pk>\d+)/delete/$', views.NotificationDeleteView.as_view(),name='notification_delete'),

        ]