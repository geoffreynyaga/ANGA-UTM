#!/usr/bin/env python3
# -*- coding:utf-8 -*-
##################################################################################
# File: /home/geoff/BursaryMashinani/BursaryMashinani/settings/base.py                             #
# Project: /home/geoff/BursaryMashinani/BursaryMashinani/settings                                  #
# Created Date: Wednesday, April 6th 2022, 1:52:43 pm                            #
# Author: Geoffrey Nyaga Kinyua ( <geoffreynyagak@gmail.com> )                     #
# -----                                                                          #
# Last Modified: Saturday August 6th 2022 7:13:02 pm                             #
# Modified By:  Geoffrey Nyaga Kinyua ( <geoffreynyagak@gmail.com> )               #
# -----                                                                          #
# This file should not be copied and/or distributed without the express          #
# permission of Geoffrey Nyaga Kinyua.                                               #
# -----                                                                          #
# Copyright (c) 2022 Geoffrey Nyaga Kinyua.                                          #
##################################################################################

import os

from decouple import Csv, config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# Application definition

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django.contrib.humanize",
]

THIRD_PARTY_APPS = [
    # "pwa",
    "debug_toolbar",
    "djgeojson",
    "bootstrap3",
    # "datetimewidget",
    "bootstrap_datepicker_plus",
    "leaflet",
    "phonenumber_field",
    "webpush",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_gis",
    "django_browser_reload",
    "tailwind",
    "theme",
    "crispy_forms",
    "crispy_tailwind",
    "drf_yasg",
]

MY_APPS = [
    "organizations",
    "accounts",
    "maps",
    "rpas",
    "flight_plans",
    "applications",
    "weather",
    "utm_messages",
    "notams",
    "notifications",
    "ui",
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + MY_APPS

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

TAILWIND_APP_NAME = "theme"

SITE_ID = 1

AUTH_USER_MODEL = "accounts.User"


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",  # for django debug toolbar
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_browser_reload.middleware.BrowserReloadMiddleware",  # for tailwind
]

ROOT_URLCONF = "ANGA_UTM.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ANGA_UTM.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# POSTGRESQL DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": config("DATABASE_NAME"),
        "USER": config("DATABASE_USER"),
        "HOST": "localhost",
        "PASSWORD": config("DATABASE_PASSWORD"),
        "PORT": "5432",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "accounts:login"
LOGIN_REDIRECT_URL = "rpas_list"

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    # "allauth.account.auth_backends.AuthenticationBackend",
]

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
    os.path.join(BASE_DIR, "theme/static"),
    os.path.join(BASE_DIR, "ui/static"),
]  # This is the directory that you should serve static files from in development.
# STATIC_ROOT and STATICFILES_DIRS cannot point to the same directory.

STATIC_ROOT = os.path.join(BASE_DIR, "static")


CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())


FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]


SERIALIZATION_MODULES = {"geojson": "django.contrib.gis.serializers.geojson"}


# max upload size 20gb
DATA_UPLOAD_MAX_MEMORY_SIZE = 21474836480  # 20 * 1024 * 1024 * 1024
MAX_UPLOAD_SIZE = 21474836480
FILE_UPLOAD_MAX_MEMORY_SIZE = 21474836480
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000


# AWS_ACCESS_KEY_ID = config('RASTER_S3_ACCESS_KEY')
# AWS_SECRET_ACCESS_KEY = config('RASTER_S3_SECRET_KEY')
# AWS_STORAGE_BUCKET_NAME = config('RASTER_S3_BUCKET')
# AWS_DEFAULT_ACL = 'public-read'
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# Swagger
SWAGGER_SETTINGS = {"SECURITY_DEFINITIONS": {"basic": {"type": "basic"}}}


REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # 'PAGE_SIZE': 50,
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",  # for  ReactNative
        "rest_framework.authentication.SessionAuthentication",  # for  react
    ),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "Your Project API",
    "DESCRIPTION": "Your project description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # OTHER SETTINGS
}

LEAFLET_CONFIG = {
    "DEFAULT_CENTER": (-0.966408, 37.048688),
    "DEFAULT_ZOOM": 20,
    "MIN_ZOOM": 8,
    "MAX_ZOOM": 23,
    "PLUGINS": {"forms": {"auto-include": True}},
    # "TILES": [
    #     (
    #         "Google Maps Satellite",
    #         "http://mt{s}.google.com/vt/lyrs=s@207000000&hl=en&x={x}&y={y}&z={z}",
    #         {
    #             "type": "xyz",
    #             "ext": "png",
    #             "attribution": f"Data CC-By-SA by <a href='http://openstreetmap.org/' target='_blank'>OpenStreetMap</a>, Tiles Courtesy of <a href='http://www.mapquest.com/'>MapQuest</a>",
    #             "subdomains": ["1", "2", "3", "4"],
    #         },
    #     ),
    #     (
    #         'Google Maps',
    #         'http://mt{s}.google.com/vt/lyrs=m@207000000&hl=en&x={x}&y={y}&z={z}',
    #         {
    #             'type': 'xyz',
    #             'ext': 'png',
    #             'attribution': 'Data CC-By-SA by <a href="http://openstreetmap.org/" target="_blank">OpenStreetMap</a>, Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a>',
    #             'subdomains': ['1', '2', '3', '4'],
    #         },
    #     ),
    # ],
    "ATTRIBUTION_PREFIX": "Swift Lab Ag &copy; <a href='https://swiftlab.tech/'>SwiftLab Limited</a>",
}


IS_TESTING = False
