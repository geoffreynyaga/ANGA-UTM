"""
WSGI config for ASTRAL_UTM project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ASTRAL_UTM.settings")

# application = get_wsgi_application()



import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ASTRAL_UTM.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise
application = get_wsgi_application()
application = DjangoWhiteNoise(application)