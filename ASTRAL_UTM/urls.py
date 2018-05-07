"""ASTRAL_UTM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from rpas import views

from applications.views import view_airspace

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('', include('pwa.urls')),  # You MUST use an empty string as the URL prefix
    url(r'^webpush/', include('webpush.urls')),

    url(r'^home$', views.home,name='home' ),

    url(r'^$', view_airspace, name='view_airspace'),

    url(r'^rpas/', include('rpas.urls')),

    url(r'^account/', include("accounts.urls", namespace ='accounts') ),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^maps/', include('maps.urls')),
    url(r'^flight_plans/', include('flight_plans.urls')),
    url(r'^weather/', include('weather.urls')),
    url(r'^applications/', include('applications.urls')),
    url(r'^messages/', include('utm_messages.urls', namespace ='messages')),

    url(r'^notams/', include('notams.urls')),
    url(r'^organizations/', include('organizations.urls')),

    url(r'^notifications/', include('notifications.urls', namespace ='notifications')),
]


if settings.DEBUG:
    urlpatterns += [

        url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,}),

        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),

    ]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns
