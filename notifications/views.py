from django.shortcuts import render

from django.views.generic import (ListView)

from .models import Notifications

# Create your views here.


class NotificationsListView(ListView):
    context_object_name = 'notifications_list'
    template_name = 'utm_messages/notifications_list.html'

    def get_queryset(self):
        return Notifications.objects.filter(receiver=self.request.user).order_by('-id')

