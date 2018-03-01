from django.conf.urls import url

from . import views
from .models import NotamAirspace

urlpatterns = [

        url(r'^airspace/datasets/$',  views.NotamLayer.as_view(model=NotamAirspace,
        properties=('notam_number','get_start_day','start_time','end')),
        name='notam_datasets'),

        url(r'^create/$', views.NotamCreateView.as_view(), name='create_notam'),


        ]
