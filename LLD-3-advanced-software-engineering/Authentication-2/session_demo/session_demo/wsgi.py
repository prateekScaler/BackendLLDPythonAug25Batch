"""
WSGI config for session_demo project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'session_demo.settings')
application = get_wsgi_application()
