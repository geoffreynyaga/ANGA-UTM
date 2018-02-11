from django.conf.urls import url

from . import views

urlpatterns = [

        url(r'^login/$', views.LoginView.as_view(), name = 'login'),
        # url(r'^logout/$', views.LogoutView.as_view(), name = 'logout'),
        url(r'^logout/$', views.logout_view, name='logout'),
        url(r'^signup/$', views.SignUp.as_view(), name='signup'),
        # url(r'^profile/$', views.view_profile.as_view(), name='view_profile'),
        url(r'^profile/(?P<pk>[\-\w]+)/update/$', views.edit_user, name='edit_profile'),
        url(r'^profile/(?P<pk>\d+)/$' , views.ViewProfile.as_view(), name='view_profile'),


        # # url(r'^rpas/$', views.rpas_list, name='rpas_list'),
        # url(r'^rpas/$', views.RpasListView.as_view(), name='rpas_list'),
        # url(r'^rpas/payload/$', views.edit_payload, name='edit_payload'),
        #
        # # url(r'(?P<pk>\d+)/$' , views.rpas_detail, name='rpas_detail'),
        # url(r'rpas/(?P<pk>\d+)/$' , views.RpasDetailView.as_view(), name='rpas_detail'),
        #
        # url(r'update/(?P<pk>\d+)/$' , views.RpasUpdateView.as_view(), name='rpas_update'),
        #
        # # url(r'(?P<rpas_pk>\d+)/(?P<manufacturer_pk>\d+)/$' , views.rpas_manufacturer_detail, name='view_manufacturer_detail'),
        # # url(r'(?P<rpas_pk>\d+)/(?P<rpas_model_pk>\d+)/$' , views.rpas_model_view, name = 'view_rpas_model'),
        # url(r'rpas/add/$', views.RpasCreateView.as_view(), name='rpas_add'),

        ]
# urlpatterns += staticfiles_urlpatterns()
