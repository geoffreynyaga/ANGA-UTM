from django.conf.urls import url
from . import views


urlpatterns = [


        url(r'^$', views.NotificationsListView.as_view(), name='notifications_list'),


        url(r'^test$', views.send_test_notification, name='notifications_test'),
]
