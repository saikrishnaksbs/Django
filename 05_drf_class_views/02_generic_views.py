"""
DRF CONCRETE GENERIC VIEWS
==========================
This script demonstrates concrete views like `ListCreateAPIView` and
`RetrieveUpdateDestroyAPIView`. These classes combine core model mixins
to provide complete CRUD capabilities with minimal boilerplate.
"""

import sys
import django
from django.conf import settings
from django.db import models
from django.urls import path
from django.core.management import execute_from_command_line, call_command
from rest_framework import generics, serializers

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
class Project(models.Model):
    title = models.CharField(max_length=100)
    lead_name = models.CharField(max_length=100)

    class Meta:
        app_label = "__main__"

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "title", "lead_name"]

# 2. Generic Views
# Simply declare queryset and serializer_class. DRF handles list, create, retrieve, update, delete.
class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

# 3. Routes configuration
urlpatterns = [
    path("api/projects/", ProjectListCreateAPIView.as_view()),
    path("api/projects/<int:pk>/", ProjectRetrieveUpdateDestroyAPIView.as_view()),
]

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # Pre-populate some records
    Project.objects.create(title="Apollo Project", lead_name="Neil Armstrong")
    Project.objects.create(title="Manhattan Project", lead_name="Robert Oppenheimer")
    
    execute_from_command_line(sys.argv)
