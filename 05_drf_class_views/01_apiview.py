"""
DRF CLASS-BASED VIEWS WITH APIVIEW
==================================
This script demonstrates how to inherit from DRF's `APIView` class
and map standard HTTP method calls (GET, POST, PUT, DELETE) to class methods.
"""

import sys
import django
from django.conf import settings
from django.db import models
from django.urls import path
from django.core.management import execute_from_command_line, call_command
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers

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
class Item(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)

    class Meta:
        app_label = "__main__"

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "quantity"]

# 2. APIView Subclass
# Subclasses of APIView map methods like get(), post() directly to HTTP verbs.
class ItemListAPIView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            return None

    def get(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk)
        if not item:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 3. Routes configuration
urlpatterns = [
    path("api/items/", ItemListAPIView.as_view()),
    path("api/items/<int:pk>/", ItemDetailAPIView.as_view()),
]

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # Pre-populate some records
    Item.objects.create(name="Notebook", quantity=10)
    Item.objects.create(name="Pen", quantity=50)
    
    execute_from_command_line(sys.argv)
