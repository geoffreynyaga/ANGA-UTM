from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DeleteView

from .models import Notifications


class NotificationsListView(ListView):
    context_object_name = "notifications_list"
    template_name = "notifications/notifications_list.html"
    # FIX ME: it seems that the app name in the url is irrevant
    """ FIXED: Its because the default template django asks for is notifications/notifications_list.html
        and that's what I had created, so changing the above to a wrong url will amke django default to default url' \
        which will always be there
    """

    def get_queryset(self):
        return Notifications.objects.filter(receiver=self.request.user).order_by("-id")


# TODO: Notifications DELETEVIEW or ajax/jquery delete and/or mark  all as read?

# TO DO: Notifications is_read
# -- FIXED


def mark_all_notifications_as_read(request):
    all_user_unread_notifications = Notifications.objects.filter(
        receiver=request.user
    ).filter(is_read=False)

    for all_user_unread_notification in all_user_unread_notifications:
        all_user_unread_notification.is_read = True
        all_user_unread_notification.save()

    return HttpResponseRedirect(reverse("notifications:notifications_list"))


class NotificationDeleteView(DeleteView):
    model = Notifications
    success_url = "/notifications/"


def test_notifications(request):
    # The group_name should be the name you would define.
    webpush = {"group": "CAA"}

    return render(
        request, "notifications/a_notification_test.html", {"webpush": webpush}
    )
