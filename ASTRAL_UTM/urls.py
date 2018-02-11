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
from django.conf.urls import url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static


from rpas import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^$', views.home,name='home' ),
    url(r'^account/', include("accounts.urls", namespace ='accounts') ),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^rpas/', include('rpas.urls')),
    # url(r'^maps/', include('maps.urls')),
    # url(r'^flight_plans/', include('flight_plans.urls')),
    # url(r'^weather/', include('weather.urls')),
    # url(r'^applications/', include('applications.urls')),
    # url(r'^messages/', include('utm_messages.urls', namespace ='messages')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
