from datetime import datetime

from django.shortcuts import render

from django.contrib.auth.models import User
from django.core.serializers import serialize
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView

# TODO: What is the diffrence between this import and the above?

from djgeojson.views import GeoJSONLayerView

from .forms import (
    ReserveAirspaceForm,
    AppliedReserveAirspaceUpdateForm,
    CAAAppliedReserveAirspaceUpdateForm,
)
from .models import ReserveAirspace


class ReserveAirspaceMainView(TemplateView):
    template_name = "applications/includes/reserve_main.html"


class ReserveAirspaceCreateView(CreateView):
    """ TO DO: Restrict Pending Flights to 10 to reduce spamming
        --FIXED by queryset count and if-else in templates
    """

    form_class = ReserveAirspaceForm
    model = ReserveAirspace
    template_name = "applications/create_reserve.html"
    success_url = "/applications/airspace"

    def form_valid(self, form):
        reserveairspace = form.save(commit=False)
        reserveairspace.created_by = User.objects.get(
            username=self.request.user
        )  # use your own profile here
        reserveairspace.save()
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(ReserveAirspaceCreateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(ReserveAirspaceCreateView, self).get_context_data(
            *args, **kwargs
        )

        my_pending_airspaces = ReserveAirspace.objects.filter(
            created_by=self.request.user
        ).filter(status=0)

        context["my_pending_approval_airspaces"] = my_pending_airspaces.order_by("-id")[
            :10
        ]
        context["my_pending_approval_airspaces_count"] = my_pending_airspaces.count()
        # context['myflightlogs'] = FlightLog.objects.filter(user=thisuser)
        return context


class ReserveAirspaceListView(ListView):
    context_object_name = "my_reserves"
    template_name = "applications/my_reserve_list.html"

    def get_queryset(self):
        return ReserveAirspace.objects.filter(created_by=self.request.user)


class ReserveAirspaceDetailView(DetailView):
    model = ReserveAirspace
    template_name = "applications/reserveairspace_detail.html"


class ReserveAirspaceUpdateView(UpdateView):
    template_name = "applications/update_my_airspace.html"
    model = ReserveAirspace
    form_class = AppliedReserveAirspaceUpdateForm
    success_url = "/applications/myreserve/"

    def form_valid(self, form):
        reserveairspace = form.save(commit=False)
        reserveairspace.created_by = User.objects.get(
            username=self.request.user
        )  # use your own profile here
        reserveairspace.save()
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(ReserveAirspaceUpdateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


##############################################################################################


# this one will just output all datasets to template
def my_reserve_datasets(request):
    airspace = serialize(
        "geojson", ReserveAirspace.objects.filter(created_by=request.user)
    )
    return HttpResponse(airspace, content_type="json")


# this one you have to pass on a pk in template to access a single instance
def my_airspace_datasets(request, pk):
    my_reserve_airspace = ReserveAirspace.objects.filter(pk=pk)
    path = serialize("geojson", my_reserve_airspace)
    return HttpResponse(path, content_type="json")


################################################################################################


def view_airspace(request):
    airspaces = ReserveAirspace.objects.all()
    return render(request, "applications/airspaces.html", {"airspaces": airspaces})


class MyModelLayer(GeoJSONLayerView):
    def get_queryset(self):
        a = ReserveAirspace.objects.exclude(expiry=True)
        # a = ReserveAirspace.objects.all()
        for x in a:
            t = datetime.combine(x.start_day, x.end) - datetime.now()
            d = t.total_seconds()
            if (d / 3600) < 0:
                x.expiry = True
                x.save()
        context = a.filter(expiry=False)
        return context


#######################################################

# CAA JUNK

# TO DO: CAA LOGIN REQUIRED MIXIN
# --FIXED: templates has_group=='CAA'
class AppliedReserveAirspaceListView(ListView):
    context_object_name = "applied_reserves"
    template_name = "applications/applied_reserve_list.html"

    def get_queryset(self):
        return ReserveAirspace.objects.filter(status=0)

    def get_context_data(self, **kwargs):
        context = super(AppliedReserveAirspaceListView, self).get_context_data(**kwargs)

        # TODO: Commercial Flights Pending Approvals

        # TODO: Private Flights Pending Approvals

        # TODO: Clubs Flights Pending Approvals

        approved_airspaces = ReserveAirspace.objects.filter(status=2).order_by("-id")

        rejected_airspaces = ReserveAirspace.objects.filter(status=1).order_by("-id")

        context["approved_airspaces"] = approved_airspaces
        context["approved_airspaces_count"] = approved_airspaces.count()

        context["rejected_airspaces"] = rejected_airspaces
        context["rejected_airspaces_count"] = rejected_airspaces.count()
        return context


class AppliedReserveAirspaceDetailView(DetailView):
    model = ReserveAirspace
    template_name = "applications/includes/detail.html"


class AppliedReserveAirspaceUpdateView(UpdateView):
    form_class = CAAAppliedReserveAirspaceUpdateForm
    model = ReserveAirspace
    template_name = "applications/approve.html"
    success_url = "/applications/applied-reserves"


##########################################################
class MyApprovalLettersListView(ListView):
    context_object_name = "my_approval_letters"
    template_name = "applications/my_approval_letters_list.html"

    def get_queryset(self):
        return ReserveAirspace.objects.filter(created_by=self.request.user, status=2)


class MyApprovalLettersDetailView(DetailView):
    model = ReserveAirspace
    template_name = "applications/appoval-letter.html"


########################################################################################
# class LogsUploadCreateView(CreateView):
#     form_class = LogsUploadForm
#     template_name = 'applications/create_log_upload.html'
#     success_url = '/applications/airspace'


# class LogsUploadListView(ListView):
#     model = LogsUpload
#     template_name = 'applications/log_uploads_list.html'
#     context_object_name = 'logs'
