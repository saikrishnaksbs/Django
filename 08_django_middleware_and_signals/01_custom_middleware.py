"""
CUSTOM CLASS-BASED DJANGO MIDDLEWARE
====================================
This script demonstrates how to write a custom Django middleware.
We calculate request processing duration and log details to the console.
"""

import sys
import time
import django
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.core.management import execute_from_command_line

# 1. Custom Middleware Class
# Django middleware are initialized with a 'get_response' callable.
class PerformanceLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Action BEFORE the view executes
        start_time = time.perf_counter()
        
        # Execute the view and get the response
        response = self.get_response(request)
        
        # Action AFTER the view executes
        duration = time.perf_counter() - start_time
        print(f"[MIDDLEWARE] Request to path '{request.path}' took {duration:.6f} seconds.")
        
        # Append custom header
        response["X-Response-Duration"] = f"{duration:.6f}s"
        return response

# 2. Configure settings containing our middleware in the stack
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        MIDDLEWARE=[
            "django.middleware.common.CommonMiddleware",
            # Register our custom middleware using its absolute import string
            "__main__.PerformanceLogMiddleware", 
        ]
    )
    django.setup()

def simple_view(request):
    time.sleep(0.02) # Simulate latency
    return HttpResponse("Look at the terminal console for custom performance logs!")

urlpatterns = [
    path("", simple_view),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
