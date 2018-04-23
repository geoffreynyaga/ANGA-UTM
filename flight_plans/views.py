from django.shortcuts import (render,redirect,render_to_response,
                            get_object_or_404)

from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext


from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.core.urlresolvers import reverse_lazy
from django.views.generic import (ListView,DetailView,
                                CreateView,UpdateView,DeleteView,)
from django.http import HttpResponse

from .forms import FlightLogCreateForm
from .models import (FlightLog,Checklist,EmmergencyInfo,PreFlight,MissionWrap)

from rpas.models import Rpas

# Create your views here.

###################### MISSION PATH ############################################
# class MissionPathDetailView(DetailView):
#     # context_object_name = 'paths'
#     model = MissionPath
#
#     def get_context_data(self, **kwargs):
#         context = super(MissionPathDetailView, self).get_context_data(**kwargs)
#         context['path_list'] = MissionPath.objects.filter(pk=self.kwargs['pk'])
#         return context


# class MissionPathListView(ListView):
#     context_object_name = 'paths'
#     model = MissionPath


# def path_datasets(request,pk):
#     mypath = MissionPath.objects.filter(pk=pk)
#     path = serialize('geojson', mypath)
#     return HttpResponse(path, content_type='json')

#
# class MissionPathCreateView(CreateView):
#     form_class = MissionPathForm
#     template_name = 'flight_plans/create_path.html'

###################### END MISSIONPATHS ########################################


###################### FLIGHT LOGS #############################################
class FlightLogListView(LoginRequiredMixin,ListView):
    context_object_name = 'mylogs'
    model = FlightLog

    def get_queryset(self):
        # queryset = super(FlightLogListView, self).get_queryset()
        queryset = FlightLog.objects.filter(user=self.request.user).order_by('-id')
        return queryset

class FlightLogDetailView(DetailView):
    model = FlightLog
    template_name = 'flight_plans/flightlog_detail.html'


class FlightLogUpdateView(UpdateView):
    fields = ('emmergency_info',
                'pre_flight','post_flight')
    model = FlightLog
    template_name = 'flight_plans/edit_flightlog.html'


class FlightLogCreateView(LoginRequiredMixin,CreateView):
    model = FlightLog
    template_name = 'flight_plans/create_flightlog.html'
    form_class = FlightLogCreateForm
    # paginate_by = 1

    def get_form_kwargs(self):
        kwargs = super(FlightLogCreateView,self).get_form_kwargs()
        kwargs['user'] = self.request.user #passing the 'user' in kwargs
        return kwargs

class PostFlightUpdateView(UpdateView):
    fields = ('damages','comments','mission_success')
    model = MissionWrap
    template_name = 'flight_plans/update_post_flight.html'

class PreFlightUpdateView(UpdateView):

    fields = ('weather','altitude','est_flight_time','area_size','no_of_flights',
                'other_info','batt_reminder')
    model = PreFlight
    template_name = 'flight_plans/update_pre_flight.html'

class EmmergencyInfoUpdateView(UpdateView):

    fields = ('closest_hosp','fire_dept','nearest_police_stn','security_service',
                'other',)
    model = EmmergencyInfo
    template_name = 'flight_plans/update_emergency_info.html'
###################### END FLIGHTLOGS ##########################################

###################### CHECKLISTS ##############################################
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

####################### END CHECKLISTS##########################################

# class MissionObjectiveCreateView(CreateView):
#     model = MissionObjective
#     fields = ('objective',)
#     template_name = 'flight_plans/create_objective.html'

# class MissionLocationCreateView(CreateView):
#     model = MissionLocation
#     fields = ('name','location')
#     template_name = 'flight_plans/create_mission_location.html'

class EmmergencyInfoCreateView(CreateView):
    model = EmmergencyInfo
    fields = ('closest_hosp','fire_dept','nearest_police_stn','location','security_service','other',)
    template_name = 'flight_plans/create_emergency_info.html'

class PreFlightCreateView(CreateView):
    model = PreFlight
    fields = ('take_off_time','sitesurvey','altitude','est_flight_time','area_size','no_of_flights','other_info','batt_reminder')
    template_name = 'flight_plans/create_pre_flight.html'


""" This is also done in the homepage ....
    Do a DRY approach
"""
@login_required()
def unfinished_logs_notifications(request):

    user_flight_logs = FlightLog.objects.filter(user=request.user)
    unfinished_pre_flight_logs = []
    unfinished_post_flight_logs = []
    for flight_log in user_flight_logs:
        if flight_log.get_pre_flight_completion() != 100:
            unfinished_pre_flight_logs.append(flight_log)
        if flight_log.get_post_flight_completion() != 100:
            unfinished_post_flight_logs.append(flight_log)

    unfinished_pre_flight_logs_count  = len(unfinished_pre_flight_logs)
    unfinished_post_flight_logs_count = len(unfinished_post_flight_logs)

    rpas_tasks = Rpas.objects.filter(user=request.user)
    unfinished_rpas_payload_tasks = []
    unfinished_rpas_model_tasks   = []
    for rpas_task in rpas_tasks.iterator():
        if rpas_task.get_rpas_model_completion() != 100.0:
            unfinished_rpas_model_tasks.append(rpas_task)

        if rpas_task.get_payload_completion() != 100.0:
            unfinished_rpas_payload_tasks.append(rpas_task)


    unfinished_rpas_payload_tasks_count = len(unfinished_rpas_payload_tasks)
    unfinished_rpas_model_tasks_count   = len(unfinished_rpas_model_tasks)


    args = {

            'unfinished_pre_flight_logs':unfinished_pre_flight_logs,
            'unfinished_post_flight_logs':unfinished_post_flight_logs,

            'unfinished_pre_flight_logs_count':unfinished_pre_flight_logs_count,
            'unfinished_post_flight_logs_count':unfinished_post_flight_logs_count,

            'unfinished_rpas_payload_tasks':unfinished_rpas_payload_tasks,
            'unfinished_rpas_model_tasks':unfinished_rpas_model_tasks,

            'unfinished_rpas_payload_tasks_count':unfinished_rpas_payload_tasks_count,
            'unfinished_rpas_model_tasks_count':unfinished_rpas_model_tasks_count,


            }


    return render(request, 'flight_plans/unfinished_logs_notifications.html', args)
