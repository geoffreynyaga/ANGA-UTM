from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import TemplateView

import logging

import json
import os

from django.shortcuts import render

import requests
from decouple import config

logger = logging.getLogger(__name__)
# This is the view that you imported in the frontend/urls.py
# def indexView(request, *args, **kwargs):
#     return render(request, "ui/index.html")  # notice the template used here

BASE_DIR = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))


def get_js_bundle():
    print(BASE_DIR, "BASE DIR")

    IS_PROD = config("IS_PROD", default=False, cast=bool)

    # IS_PROD = True

    print(f"IS_PROD: {IS_PROD}")
    logger.info(f"IS_PROD: {IS_PROD}")

    if IS_PROD is False:
        # Local file path
        url = os.path.join(BASE_DIR, "ui/static/ui/manifest.json")
        with open(url, "r") as f:
            manifest = json.load(f)
    else:
        # S3 endpoint for prod
        s3_endpoint = config("RASTER_S3_ENDPOINT_URL")
        url = f"{s3_endpoint}/static/ui/manifest.json"
        logger.info(f"Fetching manifest from S3: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            manifest = response.json()
            logger.info(f"Manifest fetched from S3: {manifest}")
        else:
            raise Exception(f"Error fetching manifest from S3: {response.status_code}")

    return manifest["main.js"]

class ReactMainView(TemplateView):
    template_name = 'ui/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # context['user_group'] = user_group
        context['user'] = user

        js_bundle = get_js_bundle()
        context["js_bundle"] = js_bundle

        return context
