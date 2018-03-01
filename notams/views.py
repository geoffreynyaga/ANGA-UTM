from django.shortcuts import render
from django.views.generic import (ListView,DetailView,
                                CreateView,UpdateView,DeleteView)
from djgeojson.views import GeoJSONLayerView
from datetime import datetime

from .models import NotamAirspace
from .forms import NotamCreateForm

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

class NotamLayer(GeoJSONLayerView):
    def get_queryset(self):
        a = NotamAirspace.objects.exclude(expiry=True)
        for x in a:
            t = datetime.combine(x.start_day, x.start_time) - datetime.now()
            d = t.total_seconds()
            if (d/3600) < 0:
                x.expiry = True
                x.save()
        context = a.filter(expiry=False)
        return context


class NotamCreateView(CreateView):
    form_class = NotamCreateForm
    template_name = 'notams/create_notam.html'
    success_url = '/applications/airspace'

    def form_valid(self, form):
            notamairspace = form.save(commit=False)
            notamairspace.created_by = User.objects.get(username=self.request.user)  # use your own profile here
            notamairspace.save()
            return HttpResponseRedirect(self.success_url)
