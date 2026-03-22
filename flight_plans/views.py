from django.contrib.auth.decorators import login_required
from django.shortcuts import render
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
