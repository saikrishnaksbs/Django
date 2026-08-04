"""
DRF APICLIENT TESTING AND SERIALIZATION BOUNDS
=============================================
This script demonstrates how to write API tests using DRF's `APIClient`
and `APITestCase` subclasses.
"""

import sys
import django
from django.conf import settings
from django.db import models
from django.urls import path
from django.core.management import call_command
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.test import APITestCase, APIClient

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
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
    )
    django.setup()

# 1. Define Model & View
class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    class Meta:
        app_label = "__main__"

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "name", "phone"]

@api_view(["POST"])
def create_contact_view(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

urlpatterns = [
    path("api/contacts/", create_contact_view),
]

# 2. Define DRF Test Case
class ContactAPITestCase(APITestCase):
    def setUp(self):
        # Construct the tables inside SQLite memory
        call_command("migrate", run_syncdb=True, verbosity=0)
        self.client = APIClient()

    def test_create_contact_success(self):
        payload = {"name": "Sherlock Holmes", "phone": "999-221B"}
        
        # APIClient POST call accepts native dictionaries, no need for json.dumps
        response = self.client.post("/api/contacts/", data=payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Sherlock Holmes")
        self.assertEqual(Contact.objects.count(), 1)

    def test_create_contact_invalid(self):
        payload = {"phone": "999-221B"} # Missing 'name' field
        
        response = self.client.post("/api/contacts/", data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

# To run tests:
# python3 -m unittest 09_django_testing/02_drf_apiclient.py
