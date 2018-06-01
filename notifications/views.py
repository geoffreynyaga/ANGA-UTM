# from django.shortcuts import render

from django.views.generic import ListView

from .models import Notifications


class NotificationsListView(ListView):
    context_object_name = 'notifications_list'
    template_name = 'notifications/notifications_list.html'
    # FIX ME: it seems that the app name in the url is irrevant
    """ FIXED: Its because the default template django asks for is notifications/notifications_list.html
        and that's what I had created, so changing the above to a wrong url will amke django default to default url' \
        which will always be there 
    """

    def get_queryset(self):
        return Notifications.objects.filter(receiver=self.request.user).order_by('-id')


# TODO: Notifications DELETEVIEW

