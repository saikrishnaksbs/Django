"""
DRF FILTERING, SEARCHING, AND ORDERING
=====================================
This script demonstrates how to configure:
1. Search query fields (SearchFilter matching strings)
2. Ordering query parameters (OrderingFilter sorting results)
3. DjangoFilterBackend to filter specific attribute keys.
"""

import sys
import django
from django.conf import settings
from django.db import models
from django.urls import path
from django.core.management import execute_from_command_line, call_command
from rest_framework import generics, serializers
from rest_framework.filters import SearchFilter, OrderingFilter

# In a standalone script, we can import django_filters if installed.
# We will check or fallback to default DRF search filters to prevent import failures.
try:
    from django_filters.rest_framework import DjangoFilterBackend
    has_django_filters = True
except ImportError:
    has_django_filters = False

if not settings.configured:
    installed_apps = [
        "django.contrib.contenttypes",
        "django.contrib.auth",
        "rest_framework",
        "__main__",
    ]
    if has_django_filters:
        installed_apps.append("django_filters")
        
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        INSTALLED_APPS=installed_apps,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
    )
    django.setup()

# 1. Define Model & Serializer
class Car(models.Model):
    make = models.CharField(max_length=50)
    model_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_digits=2)

    class Meta:
        app_label = "__main__"

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ["id", "make", "model_name", "price"]

# 2. Configure View Filters
class CarListAPIView(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    
    # Configure backends
    filter_backends = [SearchFilter, OrderingFilter]
    if has_django_filters:
        filter_backends.append(DjangoFilterBackend)
        # Match exact values on 'make'
        filterset_fields = ["make"]
        
    # 'SearchFilter' matches substrings inside these fields
    search_fields = ["model_name", "make"]
    
    # 'OrderingFilter' lets client sort using '?ordering=price' or '?ordering=-price'
    ordering_fields = ["price", "id"]
    ordering = ["id"] # Default sorting

urlpatterns = [
    path("api/cars/", CarListAPIView.as_view()),
]

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # Pre-populate car records
    Car.objects.create(make="Toyota", model_name="Corolla", price=20000)
    Car.objects.create(make="Toyota", model_name="Camry", price=26000)
    Car.objects.create(make="Tesla", model_name="Model 3", price=45000)
    Car.objects.create(make="Ford", model_name="Mustang", price=36000)
    
    print("-" * 60)
    print("[FILTER] Car API running. Queries you can run in your browser:")
    print("- Search: http://127.0.0.1:8000/api/cars/?search=toyota")
    print("- Sort by price descending: http://127.0.0.1:8000/api/cars/?ordering=-price")
    if has_django_filters:
        print("- Field filter: http://127.0.0.1:8000/api/cars/?make=Tesla")
    print("-" * 60)
    
    execute_from_command_line(sys.argv)
