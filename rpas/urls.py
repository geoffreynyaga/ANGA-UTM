from django.conf.urls import url

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from . import views

urlpatterns = [

        url(r'^main/$', views.RpasMainView.as_view(), name='rpas_main'),

        url(r'^$', views.RpasListView.as_view(), name='rpas_list'),

        url(r'^(?P<pk>\d+)/$' , views.RpasDetailView.as_view(), name='rpas_detail'),

        url(r'update/(?P<pk>\d+)/$' , views.RpasUpdateView.as_view(), name='rpas_update'),

        url(r'rpas-model/(?P<pk>\d+)/update/$' , views.RpasModelUpdateView.as_view(), name='rpas_model_update'),

        url(r'^add/$', views.RpasCreateView.as_view(), name='rpas_add'),

        url(r'^manufacturer/add/$', views.ManufacturerCreateView.as_view(), name='manufacturer_add'),
        url(r'^rpas-model/add/$', views.RpasModelCreateView.as_view(), name='rpas_model_add'),
        url(r'^payload/add/$', views.PayloadCreateView.as_view(), name='payload_add'),

        url(r'^payload/(?P<pk>\d+)/update/$' , views.PayloadUpdateView.as_view(), name='payload_update'),

        ]
