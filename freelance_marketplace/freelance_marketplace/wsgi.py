"""
WSGI config for freelance_marketplace project.

It exposes the WSGI callable as a module-level variable named ``application``.
Uses StaticFilesHandler to serve static assets when running under WSGI servers like Gunicorn.
"""

import os
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelance_marketplace.settings')

# Wrap with StaticFilesHandler so static CSS/JS files are served on Render/Gunicorn
application = StaticFilesHandler(get_wsgi_application())
