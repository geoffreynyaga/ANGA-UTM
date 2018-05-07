from django.shortcuts import render

from django.views.generic import (ListView)

from .models import Notifications

# Create your views here.


class NotificationsListView(ListView):
    context_object_name = 'notifications_list'
    template_name = 'notifications/notifications_list.html'

    def get_queryset(self):
        return Notifications.objects.filter(receiver=self.request.user).order_by('-id')

def send_test_notification(request):
    from . import send_a_notification as s
    s.send_a_notification(request.user,"test function","yeeeey")
    from django.http import HttpResponseRedirect
    return HttpResponseRedirect('/home')
