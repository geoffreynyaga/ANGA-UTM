from django.conf.urls import url

# from django.contrib.auth.views import login, logout #TODO: Login/logout/signup Use this instead???
from . import views

app_name = "accounts"

urlpatterns = [
    url(r"^login/$", views.LoginView.as_view(), name="login"),
    url(r"^logout/$", views.logout_view, name="logout"),
    url(r"^signup/$", views.SignUp.as_view(), name="signup"),
    url(r"^profile/(?P<pk>[\-\w]+)/update/$", views.edit_user, name="edit_profile"),
    url(r"^profile/(?P<pk>\d+)/$", views.ViewProfile.as_view(), name="view_profile"),
]

