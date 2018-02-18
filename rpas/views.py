from django.shortcuts import (render,redirect,HttpResponseRedirect,
                            get_object_or_404,)
from django.contrib.auth.models import User



from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms.models import inlineformset_factory

from django.views.generic import (ListView,DetailView,
                                CreateView,UpdateView,DeleteView,TemplateView)
from .forms import ManufacturerForm,PayloadForm
from .models import Rpas,Payload,Manufacturer,RpasModel

from django.core.urlresolvers import reverse


from django.contrib.auth.mixins import LoginRequiredMixin
# from . import views

# Create your views here.
@login_required()
def home(request):
    name = 'Welcome!!'
    args = {'myName':name}
    return render(request, 'home/mainhome.html', args)

# @login_required()
# def rpas_list(request):
#     args = {'myrpas': Rpas.objects.all()}
#     return render(request, 'rpas/rpas_list.html',args)

class RpasMainView(TemplateView):
    template_name = 'rpas/includes/rpas_main.html'

class RpasListView(LoginRequiredMixin,ListView):
    context_object_name = 'myrpas'
    model = Rpas

    def get_queryset(self):
        queryset = super(RpasListView, self).get_queryset()
        queryset = queryset.filter(user = self.request.user)
        return queryset

class RpasDetailView(DetailView):
    model = Rpas

class RpasCreateView(CreateView):
    fields = ('rpas_nickname',
            'rpas_model','payload','rpas_serial','rpas_pic')
    template_name = 'rpas/add_rpas.html'
    model = Rpas
    success_url = '/rpas/rpas-main'

    def form_valid(self, form):
            rpas = form.save(commit=False)
            rpas.user = User.objects.get(username=self.request.user)  # use your own profile here
            rpas.organization = rpas.user.userprofile.organization  # use your own profile here
            rpas.save()
            return HttpResponseRedirect(self.success_url)

class RpasUpdateView(UpdateView):
    fields = ('rpas_nickname','organization',
            'rpas_model','payload','rpas_serial','rpas_pic')
    model = Rpas
    template_name = 'rpas/rpas_update.html'


class ManufacturerCreateView(CreateView):
    template_name = 'rpas/add_manufacturer.html'
    # model = Manufacturer
    form_class = ManufacturerForm

class RpasModelCreateView(CreateView):
    fields = ('manufacturer','rpas_model_type','model_name','weight')
    template_name = 'rpas/add_rpas_model.html'
    model = RpasModel

class PayloadCreateView(CreateView):
    fields = ('manufacturer','payload_model','payload_serial','payload_nickname')
    template_name = 'rpas/add_payload.html'
    model = Payload


# def rpas_detail(request,pk):
#     # rpas = Rpas.objects.get(pk=pk)
#     rpas = get_object_or_404(Rpas,pk=pk)
#     return render(request, 'rpas/rpas_detail.html', {'rpas':rpas})

def rpas_manufacturer_detail(request, rpas_pk, manufacturer_pk):
    manufacturer = get_object_or_404(Manufacturer,rpas= rpas_pk,pk=manufacturer_pk)
    return render(request, 'rpas/manufacturer_details.html',{'manufacturer':manufacturer})

def rpas_model_view(request, rpas_pk, rpas_model_pk):
    rpas_model = get_object_or_404(RpasModel,rpas= rpas_pk,pk=rpas_model_pk)
    return render(request, 'rpas/rpas_model_view.html',{'rpas_model':rpas_model})


@login_required() # only logged in users should access this
def edit_payload(request):
    # querying the User object with pk from url
    user = User.objects.get(pk=1)

    manufacturer=Manufacturer.objects.get(name='DJI')
     # prepopulate UserProfileForm with retrieved user values from above.
    user_form = PayloadForm(instance=manufacturer)
    ProfileInlineFormset = inlineformset_factory(Manufacturer, Payload,
                            fields=('payload_nickname','payload_serial',
                                    'manufacturer'))

    formset = ProfileInlineFormset(instance=manufacturer)

    if request.user.is_authenticated() and request.user.id == user.id:
        if request.method == "POST":
            user_form = PayloadForm(request.POST, request.FILES, instance=manufacturer)
            formset = ProfileInlineFormset(request.POST, request.FILES, instance=manufacturer)

            if user_form.is_valid():
                created_user = user_form.save()
                formset = ProfileInlineFormset(request.POST, request.FILES, instance=created_user)

                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    print('good form')
                    return HttpResponseRedirect('/rpas/rpas/')

        return render(request, "rpas/edit_payload.html", {
            "noodle": 'DJI',
            "noodle_form": user_form,
            "formset": formset,
        })
    else:
        raise PermissionDenied
