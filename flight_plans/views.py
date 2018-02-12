from django.shortcuts import (render,redirect,render_to_response,
                            get_object_or_404)
from django.template import RequestContext


from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (ListView,DetailView,
                                CreateView,UpdateView,DeleteView,)
from django.http import HttpResponse

from .forms import MissionObjectiveForm,MissionPathForm
from .models import (FlightLog,MissionPath,
                    Checklist,MissionObjective,MissionLocation,EmmergencyInfo,PreFlight)



# Create your views here.


class MissionPathDetailView(DetailView):
    # context_object_name = 'paths'
    model = MissionPath

    def get_context_data(self, **kwargs):
        context = super(MissionPathDetailView, self).get_context_data(**kwargs)
        context['path_list'] = MissionPath.objects.filter(pk=self.kwargs['pk'])
        return context


class MissionPathListView(ListView):
    context_object_name = 'paths'
    model = MissionPath

def path_datasets(request,pk):
    mypath = MissionPath.objects.filter(pk=pk)
    path = serialize('geojson', mypath)
    # path = serialize('geojson', MissionPath.objects.filter(id=7))
    return HttpResponse(path, content_type='json')

class MissionPathCreateView(CreateView):
    # fields = ('name','path')
    # model = MissionPath
    form_class = MissionPathForm
    template_name = 'flight_plans/create_path.html'

class FlightLogListView(ListView):
    context_object_name = 'mylogs'
    model = FlightLog

    def get_queryset(self):
        queryset = super(FlightLogListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

class FlightLogDetailView(DetailView):
    model = FlightLog

class FlightLogUpdateView(UpdateView):
    fields = ('log_number','purpose','rpas','emmergency_info','pre_flight','postflight','missionpath','date')
    model = FlightLog
    template_name = 'flight_plans/edit_flightlog.html'

class FlightLogCreateView(CreateView):
    fields = ('user','log_number','purpose','date','rpas','location','emmergency_info',
            'pre_flight','postflight','missionpath')
    model = FlightLog
    template_name = 'flight_plans/create_flightlog.html'
    # paginate_by = 1

class ChecklistListView(ListView):
    model = Checklist
    template_name = 'flight_plans/checklist_list.html'
    context_object_name = 'checklists'

class ChecklistDetailView(DetailView):
    model = Checklist

class ChecklistUpdateView(UpdateView):
    model = Checklist
    fields = ('parts_check','charge_status','camera_check','props_check',
            'firmware_check','camera_check','risk_assesment','conditions_check',
            'connection_check')
    template_name = 'flight_plans/checklist_update.html'

class MissionObjectiveCreateView(CreateView):
    model = MissionObjective
    fields = ('objective',)
    template_name = 'flight_plans/create_objective.html'

class MissionLocationCreateView(CreateView):
    model = MissionLocation
    fields = ('name','location')
    template_name = 'flight_plans/create_mission_location.html'

class EmmergencyInfoCreateView(CreateView):
    model = EmmergencyInfo
    fields = ('location','closest_hosp','fire_dept','nearest_police_stn','location','security_service','other',)
    template_name = 'flight_plans/create_emergency_info.html'

class PreFlightCreateView(CreateView):
    model = PreFlight
    fields = ('take_off_time','sitesurvey','altitude','est_flight_time','area_size','no_of_flights','other_info','batt_reminder')
    template_name = 'flight_plans/create_pre_flight.html'
