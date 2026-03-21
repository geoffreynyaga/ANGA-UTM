# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

# This is the view that you imported in the frontend/urls.py
# def indexView(request, *args, **kwargs):
#     return render(request, "ui/index.html")  # notice the template used here


class ReactMainView(LoginRequiredMixin, TemplateView):
    template_name = "ui/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get user groups
        user_group = self.request.user.groups.all()
        for group in user_group:
            if group.name != "uploader":
                context["user_group"] = group.name
                continue
        # print(user_group, "user group")
        user = self.request.user
        # context['user_group'] = user_group
        context["user"] = user
        return context
