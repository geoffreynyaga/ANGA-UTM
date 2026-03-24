from django.urls import include, path, re_path

from . import views

# from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    re_path(r"^main/$", views.RpasMainView.as_view(), name="rpas_main"),
    re_path(r"^$", views.RpasListView.as_view(), name="rpas_list"),
    re_path(r"^(?P<pk>\d+)/$", views.RpasDetailView.as_view(), name="rpas_detail"),
    re_path(r"update/(?P<pk>\d+)/$", views.RpasUpdateView.as_view(), name="rpas_update"),
    re_path(
        r"rpas-model/(?P<pk>\d+)/update/$",
        views.RpasModelUpdateView.as_view(),
        name="rpas_model_update",
    ),
    re_path(r"^add/$", views.RpasCreateView.as_view(), name="rpas_add"),
    re_path(
        r"^manufacturer/add/$", views.ManufacturerCreateView.as_view(), name="manufacturer_add"
    ),
    re_path(r"^rpas-model/add/$", views.RpasModelCreateView.as_view(), name="rpas_model_add"),
    re_path(r"^payload/add/$", views.PayloadCreateView.as_view(), name="payload_add"),
    re_path(
        r"^payload/(?P<pk>\d+)/update/$", views.PayloadUpdateView.as_view(), name="payload_update"
    ),
]
