from django.urls import re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Redirect old HTML-driven URLs to the new React UI routes
    re_path(
        r"^logs/$",
        RedirectView.as_view(url="/ui/logs/", permanent=False),
        name="logs_list",
    ),
    re_path(
        r"^checklist/$",
        RedirectView.as_view(url="/ui/checklists/", permanent=False),
        name="checklist_list",
    ),
    
    # Keeping the notifications view for backend-driven status components
    re_path(
        r"^notifications/$",
        views.unfinished_logs_notifications,
        name="unfinished_logs_notifications",
    ),
]
