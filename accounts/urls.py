from django.urls import include, path, re_path

# from django.contrib.auth.views import login, logout #TODO: Login/logout/signup Use this instead???
from . import views

app_name = "accounts"

urlpatterns = [
    re_path(r"^login/$", views.LoginView.as_view(), name="login"),
    re_path(r"^logout/$", views.logout_view, name="logout"),
    re_path(r"^signup/$", views.SignUp.as_view(), name="signup"),
    re_path(r"^profile/(?P<pk>[\-\w]+)/update/$", views.edit_user, name="edit_profile"),
    re_path(r"^profile/(?P<pk>\d+)/$", views.ViewProfile.as_view(), name="view_profile"),
]
