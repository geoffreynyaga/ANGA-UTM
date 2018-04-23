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
        # .values_list('users__username',flat=True)
        # print(user_organizations.values_list('users__username',flat=True))

        all_users = {}
        for org in user_organizations:
            x = org.users.all()
            all_users.update({org:x})
            # all_users.append('org':x)
        print(all_users)
        # committee_relations = user.filter(users=self.request.user).values_list('committee__pk', flat=True)
        # item_list = Item.objects.filter(committees__in=committee_relations)

        # committee_relations = CommitteeRole.objects.filter(user=request.user).values_list('committee__pk', flat=True)
        # item_list = Item.objects.filter(committees__in=committee_relations)

        context['all_company_logs']       = FlightLog.objects.filter(user=self.request.user)
        context['my_affiliate_companies'] = Organization.objects.filter(users=self.request.user)
        context['my_postholds']           = PostHolder.objects.filter(user=self.request.user)

        context['all_employees']           = all_users

        return context
