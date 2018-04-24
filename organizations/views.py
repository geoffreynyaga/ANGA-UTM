from django.shortcuts import render

from django.views.generic import (ListView,DetailView,
                                CreateView,UpdateView,DeleteView,TemplateView)

from .models import Organization,PostHolder

from flight_plans.models import FlightLog
# Create your views here.


class AllCompanyFlightLogs(ListView):
    context_object_name = 'all_company_flight_logs'
    template_name = 'organizations/all_company_flight_logs.html'
    paginate_by = 4

    def get_queryset(self):
        return FlightLog.objects.filter(user=self.request.user).order_by('-id')

    def get_context_data(self, *args, **kwargs):
        context = super(AllCompanyFlightLogs, self).get_context_data(*args, **kwargs)

        user_organizations  = Organization.objects.filter(users=self.request.user)

        all_users = {}
        for org in user_organizations:
            x = org.users.all()
            all_users.update({org:x})

        context['all_company_logs']       = FlightLog.objects.filter(user=self.request.user)
        context['my_affiliate_companies'] = Organization.objects.filter(users=self.request.user)
        context['my_postholds']           = PostHolder.objects.filter(user=self.request.user)
        context['organization_and_users']           = all_users

        return context
