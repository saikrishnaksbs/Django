"""
HELLO WORLD IN STANDALONE DJANGO
================================
This script demonstrates running a Django application in a single file.
We configure Django settings programmatically, define a view, map a URL,
and boot up the web server.
"""

import sys
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.core.management import execute_from_command_line

# 1. Configure settings programmatically.
# A SECRET_KEY and ROOT_URLCONF are required at minimum to run a server.
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        ROOT_URLCONF=__name__, # Look inside this module for urlpatterns
        ALLOWED_HOSTS=["*"],
    )

# 2. Define a simple view
# Django views take an HttpRequest object and return an HttpResponse.
def hello_world_view(request):
    return HttpResponse("<h1>Hello World from standalone Django!</h1>")

# 3. Define URL patterns
# Django maps request paths to view functions using patterns in `urlpatterns`.
urlpatterns = [
    path("", hello_world_view),
]

# 4. Allow execution from CLI
# Running `python 01_django_basics/01_hello_world.py runserver` boots the app.
if __name__ == "__main__":
    execute_from_command_line(sys.argv)
