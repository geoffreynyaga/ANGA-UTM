from django import template

register = template.Library()

# Sidebar sections and the URL prefixes that belong to them. First match wins,
# so more specific prefixes come before the general ones.
SECTIONS = [
    ("projects", ("/applications/projects/", "/applications/clients/")),
    ("approvals", ("/applications/applied-reserves/",)),
    ("airspace", ("/applications/", "/maps/", "/notams/")),
    ("dashboard", ("/home",)),
    ("flight_logs", ("/flight_plans/logs/", "/ui/logs/")),
    ("rpas", ("/rpas/",)),
    ("components", ("/ui/inventory/",)),
    ("maintenance", ("/ui/maintenance/",)),
    ("checklists", ("/flight_plans/checklist/", "/ui/checklists/")),
    ("weather", ("/weather/",)),
    ("calendar", ("/messages/calendar/",)),
    ("mailbox", ("/messages/",)),
    ("organization", ("/organizations/",)),
]


@register.simple_tag(takes_context=True)
def nav_section(context):
    """Return the sidebar section for the current page, or an empty string."""
    request = context.get("request")
    if request is None:
        return ""
    for section, prefixes in SECTIONS:
        if request.path.startswith(prefixes):
            return section
    return ""
