"""
DRF HELLO WORLD AND @API_VIEW
=============================
This script demonstrates how to integrate Django REST Framework,
define endpoints with `@api_view`, and return DRF `Response` objects.
"""

import sys
import django
from django.conf import settings
from django.urls import path
from django.core.management import execute_from_command_line
from rest_framework.decorators import api_view
from rest_framework.response import Response

# 1. Configure settings to include 'rest_framework'
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
            "rest_framework",
            "__main__",
        ],
    )
    django.setup()

# 2. Define an API view
# The decorator enforces request formatting, formats exceptions to JSON,
# and supports return Response(...) wrappers.
@api_view(["GET", "POST"])
def hello_rest_view(request):
    if request.method == "POST":
        # request.data parses JSON payloads or form parameters automatically
        submitted_name = request.data.get("name", "World")
        return Response({
            "message": f"Hello, {submitted_name}!",
            "method": "POST",
            "data_received": request.data
        })
    
    # Defaults to GET response
    return Response({
        "message": "Hello World from Django REST Framework!",
        "method": "GET"
    })

# 3. Routes configuration
urlpatterns = [
    path("api/hello/", hello_rest_view),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
