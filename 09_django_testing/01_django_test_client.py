"""
UNIT TESTING WITH DJANGO TEST CLIENT
====================================
This script demonstrates how to define Django TestCase classes
and perform assertions using the built-in view testing client (`self.client`).
"""

import sys
import django
from django.conf import settings
from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.test import SimpleTestCase, Client

# Configure Django settings. SimpleTestCase does not require database connection.
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
    )
    django.setup()

# 1. Define target view
def calc_view(request):
    val1 = int(request.GET.get("a", 0))
    val2 = int(request.GET.get("b", 0))
    return JsonResponse({"result": val1 + val2})

urlpatterns = [
    path("api/calc/", calc_view),
]

# 2. Define Test Cases
class CalculationViewTest(SimpleTestCase):
    def setUp(self):
        # Instantiate test client
        self.client = Client()

    def test_calculator_success(self):
        # Execute GET request
        response = self.client.get("/api/calc/?a=5&b=10")
        
        # Verify HTTP status code
        self.assertEqual(response.status_code, 200)
        
        # Verify JSON content
        data = response.json()
        self.assertEqual(data["result"], 15)

    def test_calculator_default_values(self):
        response = self.client.get("/api/calc/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["result"], 0)

# To run tests:
# python3 -m unittest 09_django_testing/01_django_test_client.py
