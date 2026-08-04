"""
DRF PERMISSIONS AND CUSTOM GUARDS
=================================
This script demonstrates how to configure route access guards.
We cover built-in permissions (IsAuthenticated, IsAdminUser) and implement
a custom object-level permission (`IsOwnerOrReadOnly`).
"""

import sys
import django
from django.conf import settings
from django.db import models
from django.urls import path
from django.core.management import execute_from_command_line, call_command
from rest_framework import serializers, status, generics
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
from django.contrib.auth.models import User

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
class UserPost(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()

    class Meta:
        app_label = "__main__"

class UserPostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = UserPost
        fields = ["id", "owner", "title", "body"]

# 2. Custom Permission Guard
# Custom permissions inherit from BasePermission and override:
# - 'has_permission' for global request level checks
# - 'has_object_permission' for single object record level checks
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only methods (GET, HEAD, OPTIONS) are always allowed
        if request.method in SAFE_METHODS:
            return True
            
        # Write methods are only allowed if the requesting user is the owner
        return obj.owner == request.user

# 3. Protected endpoint
# Uses IsAuthenticated for global check, and IsOwnerOrReadOnly for record update/delete checks.
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserPost.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

urlpatterns = [
    path("api/posts/<int:pk>/", PostDetailView.as_view()),
]

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    execute_from_command_line(sys.argv)
