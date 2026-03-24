from datetime import datetime

from decouple import config
from django.contrib.auth import get_user_model

User = get_user_model()
from django.core.serializers import serialize
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.base import TemplateView

# TODO: What is the diffrence between this import and the above?
from djgeojson.views import GeoJSONLayerView

from rpas.models import Rpas

from .forms import (
    AppliedReserveAirspaceUpdateForm,
    CAAAppliedReserveAirspaceUpdateForm,
    ReserveAirspaceForm,
    ClientForm,
    ProjectForm,
)
from .models import ReserveAirspace, Client, Project


class ProjectsIndexView(TemplateView):
    template_name = "applications/projects_index.html"


class ClientListView(ListView):
    model = Client
    template_name = "applications/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return Client.objects.filter(created_by=self.request.user)


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = "applications/client_form.html"
    success_url = "/applications/clients/list/"

    def form_valid(self, form):
        client = form.save(commit=False)
        client.created_by = self.request.user
        client.save()
        return HttpResponseRedirect(self.success_url)


class ProjectListView(ListView):
    model = Project
    template_name = "applications/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user)


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "applications/project_form.html"
    success_url = "/applications/projects/list/"

    def form_valid(self, form):
        project = form.save(commit=False)
        project.created_by = self.request.user
        # Organization is auto-assigned in model save() via user profile
        project.save()
        return HttpResponseRedirect(self.success_url)


class ReserveAirspaceMainView(TemplateView):
    template_name = "applications/includes/reserve_main.html"


class OldReserveAirspaceCreateView(CreateView):
    """TO DO: Restrict Pending Flights to 10 to reduce spamming
    --FIXED by queryset count and if-else in templates
    """

    form_class = ReserveAirspaceForm
    model = ReserveAirspace
    template_name = "applications/create_reserve.html"
    success_url = "/applications/airspace"

    def form_valid(self, form):
        reserveairspace = form.save(commit=False)
        reserveairspace.created_by = User.objects.get(
            email=self.request.user
        )  # use your own profile here
        reserveairspace.save()
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(OldReserveAirspaceCreateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(OldReserveAirspaceCreateView, self).get_context_data(
            *args, **kwargs
        )

        my_pending_airspaces = ReserveAirspace.objects.filter(
            created_by=self.request.user
        ).filter(status=0)

        context["my_pending_approval_airspaces"] = my_pending_airspaces.order_by("-id")[
            :10
        ]
        context["my_pending_approval_airspaces_count"] = my_pending_airspaces.count()
        # context['myflightlogs'] = DailyWorkLog.objects.filter(user=thisuser)
        return context


class ReserveAirspaceCreateView(CreateView):
    """TO DO: Restrict Pending Flights to 10 to reduce spamming
    --FIXED by queryset count and if-else in templates
    """

    form_class = ReserveAirspaceForm
    model = ReserveAirspace
    template_name = "applications/create_reserve.html"
    # success_url = "/applications/airspace"

    def form_valid(self, form):
        reserveairspace = form.save(commit=False)
        reserveairspace.created_by = User.objects.get(
            email=self.request.user
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

        org = self.request.user.userprofile.organization

        context["my_pending_approval_airspaces"] = my_pending_airspaces.order_by("-id")[
            :10
        ]
        context["my_pending_approval_airspaces_count"] = my_pending_airspaces.count()
        # context['myflightlogs'] = DailyWorkLog.objects.filter(user=thisuser)

        context["my_rpas"] = Rpas.objects.filter(organization=org)
        from .models import Project

        context["my_projects"] = Project.objects.filter(
            organization=org, is_complete=False
        )

        context["AIRMAP_API_KEY"] = config("AIRMAP_API_KEY")
        context["MAPBOX_ACCESS_TOKEN"] = config("MAPBOX_ACCESS_TOKEN")

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
            email=self.request.user
        )  # use your own profile here
        reserveairspace.save()
        return HttpResponseRedirect(self.success_url)

    def get_form_kwargs(self):
        kwargs = super(ReserveAirspaceUpdateView, self).get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


##############################################################################################


# this one will just output all User datasets to template
def my_reserve_datasets(request):
    airspace = serialize(
        "geojson", ReserveAirspace.objects.filter(created_by=request.user)
    )
    return HttpResponse(airspace, content_type="json")


def all_reserve_datasets(request):
    airspace = serialize(
        "geojson",
        ReserveAirspace.objects.filter(expiry=False),
        geometry_field="geom",
    )
    return HttpResponse(airspace, content_type="json")


# this one you have to pass on a pk in template to access a single instance
def my_airspace_datasets(request, pk):
    my_reserve_airspace = ReserveAirspace.objects.filter(pk=pk)
    path = serialize("geojson", my_reserve_airspace)
    return HttpResponse(path, content_type="json")


################################################################################################


def view_airspace(request):
    # from applications import bounding

    # import json

    # print(type(bounding.bounding_boxes), "should be dict")
    # print(type(json.dumps(bounding.bounding_boxes)), "should be str")

    airspaces = ReserveAirspace.objects.all()
    AIRMAP_API_KEY = config("AIRMAP_API_KEY")
    MAPBOX_ACCESS_TOKEN = config("MAPBOX_ACCESS_TOKEN")

    return render(
        request,
        "applications/airspaces.html",
        {
            "airspaces": airspaces,
            "AIRMAP_API_KEY": AIRMAP_API_KEY,
            "MAPBOX_ACCESS_TOKEN": MAPBOX_ACCESS_TOKEN,
            # "bounding_boxes": json.dumps(bounding.bounding_boxes),
        },
    )


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
