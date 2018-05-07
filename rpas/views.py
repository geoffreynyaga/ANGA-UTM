from django.shortcuts import (render,HttpResponseRedirect,
                              get_object_or_404,)
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView, TemplateView)
from .forms import ManufacturerForm,PayloadForm,RpasCreateForm
from .models import Rpas,Payload,Manufacturer,RpasModel

from django.contrib.auth.mixins import LoginRequiredMixin

from utm_messages.models import UserToUserMessages
from flight_plans.models import FlightLog
from notifications.models import Notifications


# Create your views here.
@login_required()
def home(request):
    name = 'Welcome!!'
    x = UserToUserMessages.objects.filter(receiver=request.user).filter(is_read=False).order_by('-id')[:5]
    y = x.count()

    unread_notifications = Notifications.objects.filter(receiver=request.user).filter(is_read=False).order_by('-id')[:5]
    unread_notifications_count = unread_notifications.count()

##################### RPAS/PAYLOAD CREATE COMPLETION TASKS######################
    """ come up with a better way to iterate or queryset the damn Tasks
        Perhaps create an boolean or better a float field where the get_completion
        methods save the values to the model and we access the modelfield value from
        get_queryset  filter.... """

    rpas_tasks = Rpas.objects.filter(user=request.user)
    unfinished_rpas_payload_tasks = []
    unfinished_rpas_model_tasks   = []
    for rpas_task in rpas_tasks.iterator():
        if rpas_task.get_payload_completion() != 100.0:
            unfinished_rpas_payload_tasks.append(rpas_task)

        if rpas_task.get_rpas_model_completion() != 100.0:
            unfinished_rpas_model_tasks.append(rpas_task)

    all_rpas_tasks_count = len(unfinished_rpas_payload_tasks) + len(unfinished_rpas_model_tasks)

###############################################################################
    user_flight_logs = FlightLog.objects.filter(user=request.user)
    unfinished_pre_flight_logs = []
    unfinished_post_flight_logs = []
    for flight_log in user_flight_logs:
        if flight_log.get_pre_flight_completion() != 100:
            unfinished_pre_flight_logs.append(flight_log)
        if flight_log.get_post_flight_completion() != 100:
            unfinished_post_flight_logs.append(flight_log)

    all_flightlog_tasks_count = len(unfinished_pre_flight_logs) + len(unfinished_post_flight_logs)
    all_tasks_count = all_rpas_tasks_count + all_flightlog_tasks_count

    args = {'myName':name, 'unread_messages':x, 'unread_messages_number':y,
            'unread_notifications': unread_notifications,
            'unread_notifications_count':unread_notifications_count,

            'all_tasks_count':all_tasks_count,
            'unfinished_rpas_payload_tasks':unfinished_rpas_payload_tasks,
            'unfinished_rpas_model_tasks':unfinished_rpas_model_tasks,

            'unfinished_pre_flight_logs':unfinished_pre_flight_logs,
            'unfinished_post_flight_logs':unfinished_post_flight_logs,
            }

    return render(request, 'home/mainhome.html', args)


class RpasMainView(TemplateView):
    template_name = 'rpas/includes/rpas_main.html'


class RpasListView(LoginRequiredMixin,ListView):
    context_object_name = 'myrpas'
    model = Rpas

    def get_queryset(self):
        queryset = super(RpasListView, self).get_queryset()
        queryset = queryset.filter(user = self.request.user)
        return queryset


class RpasDetailView(DetailView):
    model = Rpas


class RpasCreateView(CreateView):
    # fields = ('rpas_nickname', 'rpas_serial','rpas_pic')
    template_name = 'rpas/add_rpas.html'
    model = Rpas
    form_class = RpasCreateForm
    success_url = '/rpas'

    def form_valid(self, form):
            rpas = form.save(commit=False)
            rpas.user = User.objects.get(username=self.request.user)  # use your own profile here
            # rpas.organization = rpas.user.userprofile.organization  # use your own profile here
            #########################################################################################
            """ but in organizations model i have put multiple organizations but one in userprofile
                Perhaps doa queryset here and listview organizations in profile
                
                --FIXED
            """
            ########################################################################################
            rpas.save()
            return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(RpasCreateView, self).get_form_kwargs()
        kwargs['rpas_user'] = self.request.user
        return kwargs


class RpasUpdateView(UpdateView):
    fields = ('rpas_nickname','organization',
            'rpas_model','payload','rpas_serial','rpas_pic')
    model = Rpas
    template_name = 'rpas/rpas_update.html'


class RpasModelUpdateView(UpdateView):
    fields = ('manufacturer','rpas_model_type','model_name','weight')
    model = RpasModel
    template_name = 'rpas/rpas_model_update.html'


class ManufacturerCreateView(CreateView):
    template_name = 'rpas/add_manufacturer.html'
    form_class = ManufacturerForm


class RpasModelCreateView(CreateView):
    fields = ('manufacturer','rpas_model_type','model_name','weight')
    template_name = 'rpas/add_rpas_model.html'
    model = RpasModel


class PayloadCreateView(CreateView):
    # fields = ('manufacturer','payload_model','payload_serial','payload_nickname')
    template_name = 'rpas/add_payload.html'
    model = Payload
    form_class = PayloadForm


class PayloadUpdateView(UpdateView):
    fields = ('payload_model','payload_serial','payload_nickname')
    model = Payload
    template_name = 'rpas/payload_update.html'


def rpas_manufacturer_detail(request, rpas_pk, manufacturer_pk):
    manufacturer = get_object_or_404(Manufacturer,rpas= rpas_pk,pk=manufacturer_pk)
    return render(request, 'rpas/manufacturer_details.html',{'manufacturer':manufacturer})


def rpas_model_view(request, rpas_pk, rpas_model_pk):
    rpas_model = get_object_or_404(RpasModel,rpas= rpas_pk,pk=rpas_model_pk)
    return render(request, 'rpas/rpas_model_view.html',{'rpas_model':rpas_model})

