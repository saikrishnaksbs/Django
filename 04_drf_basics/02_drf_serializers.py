"""
DRF SERIALIZERS AND VALIDATION
==============================
This script demonstrates how to define ModelSerializers, perform validation,
and handle serialization and deserialization workflows.
"""

import sys
import django
from django.conf import settings
from django.db import models
from django.urls import path
from django.core.management import execute_from_command_line, call_command
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

# 1. Define Model
class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "__main__"

# 2. Define ModelSerializer
# Automatically matches field shapes to DB columns.
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "completed", "created_at"]
        read_only_fields = ["id", "created_at"]

    # Custom field-level validator for 'title'
    def validate_title(self, value):
        if "spam" in value.lower():
            raise serializers.ValidationError("Title cannot contain the word 'spam'.")
        return value

# 3. Define endpoints using the serializer
@api_view(["GET", "POST"])
def task_list_view(request):
    if request.method == "POST":
        # Deserialization and validation
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            # Save valid data to DB
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Serialization (GET)
    tasks = Task.objects.all()
    # pass many=True since we are serializing a list of tasks
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

urlpatterns = [
    path("api/tasks/", task_list_view),
]

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # Pre-populate with one task
    Task.objects.create(title="Learn Django ORM", description="Complete module 02.")
    
    execute_from_command_line(sys.argv)
