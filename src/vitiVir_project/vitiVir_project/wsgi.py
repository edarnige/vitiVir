"""
WSGI config for vitiVir_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os, sys

# add the virtualenv site-packages path to the sys.path
sys.path.append('/var/www/venv/lib/python3.6/site-packages')
sys.path.append('/static')
sys.path.append('/var/www/vitiVir')

# run app on port 9000
from django.core.management.commands.runserver import Command as runserver
runserver.default_addr = "9000"
runserver.default_port = "9000"

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vitiVir_project.settings')

application = get_wsgi_application()
