"""
WSGI config for lunalux project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

HOME = os.environ.get("HOME")
load_dotenv(os.path.join(HOME, "/lunalux.io/.env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunalux.settings.production")

application = get_wsgi_application()
