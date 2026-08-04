"""
DRF TOKEN AUTHENTICATION
========================
This script demonstrates how to configure DRF's `TokenAuthentication`.
We register the authtoken app, generate a database token for a user,
and protect an endpoint requiring the correct HTTP 'Authorization' header.
"""

import sys
import django
from django.conf import settings
from django.urls import path
from django.core.management import execute_from_command_line, call_command

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
            "rest_framework.authtoken", # Enables Token DB table
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

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

# 1. Protect view with Token authentication
class SecureDashboard(APIView):
    # Register Authentication & Permission guards
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user is set to the matching authenticated User instance
        return Response({
            "message": f"Welcome to the secure dashboard, {request.user.username}!",
            "user_email": request.user.email,
            "token_used": request.auth.key # request.auth holds the Token instance
        })

urlpatterns = [
    path("api/dashboard/", SecureDashboard.as_view()),
]

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    
    # 2. Setup mock user and generate a token
    user = User.objects.create_user(username="dev_user", email="dev@test.org", password="mypassword")
    token = Token.objects.create(user=user)
    
    print("-" * 60)
    print(f"[AUTH] Generated User: {user.username}")
    print(f"[AUTH] Generated Token Key: {token.key}")
    print(f"[AUTH] To access endpoint, send GET request to http://127.0.0.1:8000/api/dashboard/")
    print(f"[AUTH] with header -> Authorization: Token {token.key}")
    print("-" * 60)
    
    execute_from_command_line(sys.argv)
