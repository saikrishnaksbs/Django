"""
DRF PAGINATION SCHEMES
======================
This script demonstrates how to define and configure pagination classes.
We cover PageNumberPagination and show how it modifies the JSON response schema.
"""

import sys
import django
from django.conf import settings
from django.db import models
from django.urls import path
from django.core.management import execute_from_command_line, call_command
from rest_framework import generics, serializers
from rest_framework.pagination import PageNumberPagination

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

# 1. Define Model & Serializer
class Event(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()

    class Meta:
        app_label = "__main__"

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "year"]

# 2. Custom Pagination Class
# Override settings like default page size and query parameter names.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2                      # Small page size for easy demonstration
    page_size_query_param = "page_size" # Let clients request custom size (e.g. ?page_size=10)
    max_page_size = 100

# 3. View registering custom pagination class
class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all().order_by("id")
    serializer_class = EventSerializer
    pagination_class = StandardResultsSetPagination

urlpatterns = [
    path("api/events/", EventListAPIView.as_view()),
]

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # Pre-populate 5 event records
    for i in range(1, 6):
        Event.objects.create(name=f"Expo Event {i}", year=2020 + i)
        
    execute_from_command_line(sys.argv)
