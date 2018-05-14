from django.shortcuts import render

from django.contrib.auth import login,logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile
from rpas.models import Rpas
from flight_plans.models import FlightLog
from .forms import UserForm
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from . import forms

# Create your views here.


class LoginView(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('view_airspace')
    template_name = "accounts/login.html"

    def get_form (self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request,**self.get_form_kwargs())

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/account/login')


class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'


@login_required() # only logged in users should access this
def edit_user(request, pk):
    # querying the User object with pk from url
    user = User.objects.get(pk=pk)

    # prepopulate UserProfileForm with retrieved user values from above.
    user_form = UserForm(instance=user)

    # The sorcery begins from here, see explanation below
    ProfileInlineFormset = inlineformset_factory(User, UserProfile,
                            fields=('phone_number','organization','bio','profile_pic',
                            'location', 'birth_date'))

    formset = ProfileInlineFormset(instance=user)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=user)

            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    # return HttpResponseRedirect('/account/profile/')
                    return HttpResponseRedirect(reverse('accounts:view_profile', args=(user.id,)))
                    

        return render(request, "accounts/edit_profile.html", {
            "noodle": pk,
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied


# class view_profile(generic.TemplateView):
#     template_name = "accounts/profile.html"
#     # model = UserProfile
#
#     def get(self, request):
#         myrpas = Rpas.objects.filter(organization = request.user.userprofile.organization)
#         myflightlogs = FlightLog.objects.filter(user = request.user)
#         args = {'myrpas': myrpas, 'myflightlogs':myflightlogs}
#         return render(request, self.template_name ,args)


class ViewProfile(LoginRequiredMixin,generic.DetailView):
    template_name = "accounts/profile.html"
    model = UserProfile

    def get_context_data(self,*args,**kwargs):
        context = super(ViewProfile,self).get_context_data(**kwargs)
        pk = self.kwargs['pk']
        thisuser = User.objects.get(pk=pk)
        org = thisuser.userprofile.organization
        context['myrpas'] = Rpas.objects.filter(organization = org)
        context['myflightlogs'] = FlightLog.objects.filter(user = thisuser)
        return (context)
