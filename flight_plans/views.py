from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from applications.models import ReserveAirspace
from .models import DailyWorkLog
from rpas.models import Rpas

# Minimal views for flight_plans. 
# Most management logic has been migrated to React/DRF API.

@login_required()
def unfinished_logs_notifications(request):
    """
    Renders logic for identifying incomplete pre/post flight logs 
    and mission-critical RPAS data. Used mainly for dashboard/navbar.
    """
    user_flight_logs = DailyWorkLog.objects.filter(user=request.user)
    
    unfinished_pre_flight_logs = [log for log in user_flight_logs if log.get_pre_flight_completion() != 100]
    unfinished_post_flight_logs = [log for log in user_flight_logs if log.get_post_flight_completion() != 100]

    rpas_tasks = Rpas.objects.filter(user=request.user)
    unfinished_rpas_payload_tasks = [r for r in rpas_tasks if r.get_payload_completion() != 100.0]
    unfinished_rpas_model_tasks = [r for r in rpas_tasks if r.get_rpas_model_completion() != 100.0]

    args = {
        "unfinished_pre_flight_logs": unfinished_pre_flight_logs,
        "unfinished_post_flight_logs": unfinished_post_flight_logs,
        "unfinished_pre_flight_logs_count": len(unfinished_pre_flight_logs),
        "unfinished_post_flight_logs_count": len(unfinished_post_flight_logs),
        "unfinished_rpas_payload_tasks": unfinished_rpas_payload_tasks,
        "unfinished_rpas_model_tasks": unfinished_rpas_model_tasks,
        "unfinished_rpas_payload_tasks_count": len(unfinished_rpas_payload_tasks),
        "unfinished_rpas_model_tasks_count": len(unfinished_rpas_model_tasks),
    }

    return render(request, "flight_plans/unfinished_logs_notifications.html", args)


class FlightLogListView(LoginRequiredMixin, ListView):
    """Every flight the user has planned, filtered by the All / Upcoming / Completed tabs."""

    template_name = "flight_plans/flightlog_list.html"
    context_object_name = "flights"
    paginate_by = 25
    TABS = ("All", "Upcoming", "Completed")

    def get_tab(self):
        tab = self.request.GET.get("tab", "All")
        return tab if tab in self.TABS else "All"

    def get_queryset(self):
        today = date.today()
        flights = (
            ReserveAirspace.objects.filter(created_by=self.request.user)
            .select_related("project")
            .prefetch_related("rpas")
        )
        tab = self.get_tab()
        if tab == "Upcoming":
            return flights.filter(
                start_day__gte=today,
                status__in=[ReserveAirspace.PENDING, ReserveAirspace.APPROVED],
            ).order_by("start_day", "start_time")
        if tab == "Completed":
            flights = flights.filter(start_day__lt=today, status=ReserveAirspace.APPROVED)
        return flights.order_by("-start_day", "-start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tab"] = self.get_tab()
        context["tabs"] = self.TABS
        context["today"] = date.today()
        return context
