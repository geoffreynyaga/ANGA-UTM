from django.shortcuts import render

from django.views.generic import (ListView,DetailView,
                                CreateView,UpdateView,DeleteView)
from django.views.generic.base import TemplateView

from .models import ReserveAirspace,LogsUpload
from .forms import ReserveAirspaceForm,AppliedReserveAirspaceUpdateForm,LogsUploadForm

from django.core.serializers import serialize
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


class ReserveAirspaceMainView(TemplateView):
    template_name = 'applications/includes/reserve_main.html'

class ReserveAirspaceCreateView(CreateView):
    form_class = ReserveAirspaceForm
    model = ReserveAirspace
    template_name = 'applications/create_reserve.html'
    success_url = '/applications/airspace'

    def form_valid(self, form):
            reserveairspace = form.save(commit=False)
            reserveairspace.created_by = User.objects.get(username=self.request.user)  # use your own profile here
            reserveairspace.save()
            return HttpResponseRedirect(self.success_url)

class ReserveAirspaceListView(ListView):
    context_object_name = 'my_reserves'
    template_name = 'applications/my_reserve_list.html'

    def get_queryset(self):
        return ReserveAirspace.objects.filter(created_by=self.request.user)

def my_reserve_datasets(request):
    airspace = serialize('geojson', ReserveAirspace.objects.filter(created_by=request.user))
    return HttpResponse(airspace, content_type='json')

class ReserveAirspaceDetailView(DetailView):
    model = ReserveAirspace
    template_name = 'applications/reserveairspace_detail.html'


class ReserveAirspaceUpdateView(UpdateView):
    template_name = 'applications/update_my_airspace.html'
    model = ReserveAirspace
    form_class = ReserveAirspaceForm

def my_airspace_datasets(request,pk):
    my_reserve_airspace = ReserveAirspace.objects.filter(pk=pk)
    path = serialize('geojson', my_reserve_airspace)
    return HttpResponse(path, content_type='json')



def view_airspace(request):
    airspaces = ReserveAirspace.objects.all()
    return render(request, 'applications/airspaces.html',{'airspaces':airspaces})

from djgeojson.views import GeoJSONLayerView
class MyModelLayer(GeoJSONLayerView):
    def get_queryset(self):
        context = ReserveAirspace.objects.filter(expiry=False)
        return context

# def airspace_datasets(request):
#     airspace = serialize('geojson', ReserveAirspace.objects.all())
#     return HttpResponse(airspace, content_type='json')


class AppliedReserveAirspaceListView(ListView):
    context_object_name = 'applied_reserves'
    template_name = 'applications/applied_reserve_list.html'

    def get_queryset(self):
        return ReserveAirspace.objects.filter(status=0)


class AppliedReserveAirspaceDetailView(DetailView):
    model = ReserveAirspace
    template_name = 'applications/includes/detail.html'


class AppliedReserveAirspaceUpdateView(UpdateView):
    form_class = AppliedReserveAirspaceUpdateForm
    model = ReserveAirspace
    # template_name = 'applications/applied_reserveairspace_update.html'
    template_name = 'applications/approve.html'

    success_url = '/applications/applied-reserves'


class MyApprovalLettersListView(ListView):
    context_object_name = 'my_approval_letters'
    template_name = 'applications/my_approval_letters_list.html'

    def get_queryset(self):
        return ReserveAirspace.objects.filter(created_by=self.request.user,status=2)

class MyApprovalLettersDetailView(DetailView):
    model = ReserveAirspace
    template_name = 'applications/appoval-letter.html'

class LogsUploadCreateView(CreateView):
    form_class = LogsUploadForm
    template_name = 'applications/create_log_upload.html'
    success_url = '/applications/airspace'

class LogsUploadListView(ListView):
    model = LogsUpload
    template_name = 'applications/logs_list.html'
    context_object_name = 'logs'
