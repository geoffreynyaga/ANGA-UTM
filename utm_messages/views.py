from django.shortcuts import render
from django.views.generic import (ListView,DetailView,
                                CreateView,UpdateView,DeleteView,TemplateView)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import UserToUserMessages,Notifications
from .forms import UserToUserMessagesForm
# Create your views here.

class MessagesCreateView(CreateView):
    form_class = UserToUserMessagesForm
    template_name = 'utm_messages/compose.html'
    success_url = '/messages/'

    def form_valid(self, form):
            usertousermessages = form.save(commit=False)
            usertousermessages.sender = User.objects.get(username=self.request.user)  # use your own profile here
            usertousermessages.save()
            return HttpResponseRedirect(self.success_url)


class SentMessagesListView(ListView):
    context_object_name = 'sent'
    template_name = 'utm_messages/sent.html'

    def get_queryset(self):
        return UserToUserMessages.objects.filter(sender=self.request.user).order_by('-id')

class InboxListView(ListView):
    context_object_name = 'inbox'
    template_name = 'utm_messages/inbox.html'

    def get_queryset(self):
        return UserToUserMessages.objects.filter(receiver=self.request.user).order_by('-id')

class MessageDetailView(DetailView):
    model = UserToUserMessages
    template_name = 'utm_messages/message_detail.html'

    def get_object(self, queryset=None):
        obj = super(MessageDetailView, self).get_object(queryset=queryset)
        obj.is_read = True
        obj.save()
        return obj


class MessagesMainView(TemplateView):
    template_name = 'utm_messages/main.html'


class CalendarView(TemplateView):
    template_name = 'utm_messages/calendar.html'

class NotificationsListView(ListView):
    context_object_name = 'notifications_list'
    template_name = 'utm_messages/notifications_list.html'

    def get_queryset(self):
        return Notifications.objects.filter(receiver=self.request.user).order_by('-id')
