from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login, logout

from . import views

urlpatterns = [


        # url(r'^rpas/$', views.rpas_list, name='rpas_list'),
        url(r'^rpas-main/$', views.RpasMainView.as_view(), name='rpas_main'),

        url(r'^rpas/$', views.RpasListView.as_view(), name='rpas_list'),
        url(r'^rpas/payload/$', views.edit_payload, name='edit_payload'),

        # url(r'(?P<pk>\d+)/$' , views.rpas_detail, name='rpas_detail'),
        url(r'rpas/(?P<pk>\d+)/$' , views.RpasDetailView.as_view(), name='rpas_detail'),

        url(r'update/(?P<pk>\d+)/$' , views.RpasUpdateView.as_view(), name='rpas_update'),

        # url(r'(?P<rpas_pk>\d+)/(?P<manufacturer_pk>\d+)/$' , views.rpas_manufacturer_detail, name='view_manufacturer_detail'),
        # url(r'(?P<rpas_pk>\d+)/(?P<rpas_model_pk>\d+)/$' , views.rpas_model_view, name = 'view_rpas_model'),
        url(r'rpas/add/$', views.RpasCreateView.as_view(), name='rpas_add'),

        url(r'rpas/manufacturer/add/$', views.ManufacturerCreateView.as_view(), name='manufacturer_add'),
        url(r'rpas/rpas-model/add/$', views.RpasModelCreateView.as_view(), name='rpas_model_add'),
        url(r'rpas/payload/add/$', views.PayloadCreateView.as_view(), name='payload_add'),



        ]
# urlpatterns += staticfiles_urlpatterns()
