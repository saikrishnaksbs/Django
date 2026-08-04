"""
DRF VIEWSETS AND ROUTERS
========================
This script demonstrates combining multiple API endpoints into a single class using ViewSets,
and automatically generating URL routing tables with the `DefaultRouter` class.
"""

import sys
import django
from django.conf import settings
from django.db import models
from django.core.management import execute_from_command_line, call_command
from rest_framework import viewsets, serializers
from rest_framework.routers import DefaultRouter

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
class Employee(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.CharField(max_length=50)

    class Meta:
        app_label = "__main__"

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name", "department"]

# 2. ModelViewSet
# ModelViewSet automatically handles all CRUD actions (.list(), .create(), .retrieve(), etc.)
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

# 3. Router Configuration
# Instantiating DefaultRouter and registering our viewset.
# This automatically creates path definitions (e.g. GET /employees/, GET /employees/{id}/, etc.)
router = DefaultRouter()
router.register(r"employees", EmployeeViewSet, basename="employee")

# Use router.urls for urlpatterns
urlpatterns = router.urls

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # Pre-populate records
    Employee.objects.create(first_name="Jane", last_name="Doe", department="Engineering")
    Employee.objects.create(first_name="John", last_name="Smith", department="HR")
    
    execute_from_command_line(sys.argv)
