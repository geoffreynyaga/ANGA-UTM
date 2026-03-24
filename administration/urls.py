from django.urls import path, include

app_name = 'administration'

urlpatterns = [
    path('api/', include('administration.api.urls')),
]
