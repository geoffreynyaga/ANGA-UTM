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
        users_list = []
        for org in user_organizations:
            x = org.users.all()
            users_list.append(x)
            all_users.update({org:x})

        refined_user_list = []
        for user_queryset_per_org in users_list:
            for user in user_queryset_per_org:
                if not user in refined_user_list:
                    refined_user_list.append(user)


        all_company_logs = []
        for org_user in refined_user_list:
            x = (FlightLog.objects.filter(user=org_user))
            if x:
                for log in x:
                    all_company_logs.append(log)

        context['my_affiliate_companies'] = Organization.objects.filter(users=self.request.user)
        context['my_postholds']           = PostHolder.objects.filter(user=self.request.user)
        context['organization_and_users'] = all_users
        context['all_company_logs']       = all_company_logs
        context['all_employees']          = refined_user_list


        return context