"""
PATH ROUTING AND PARAMETERS
===========================
This script demonstrates Django's URL routing, including typed path converters
which capture variables from the URL path.
"""

import sys
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.core.management import execute_from_command_line

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
    )

# 1. Dynamic Views
# Captured variables are passed as arguments to the view function.
def get_item_by_id(request, item_id: int):
    # item_id is automatically parsed as an integer by the <int:...> converter
    return HttpResponse(f"Fetching item with numeric ID: {item_id}")

def get_user_profile(request, username: str):
    # Matches strings without path separators
    return HttpResponse(f"Profile page of user: {username}")

def get_article_by_slug(request, article_slug: str):
    # Matches letters, numbers, hyphens, and underscores
    return HttpResponse(f"Showing article with slug: {article_slug}")

# 2. Path routing configuration
urlpatterns = [
    # Path converters restrict inputs: <int:...>, <str:...>, <slug:...>, <uuid:...>, <path:...>
    path("items/<int:item_id>/", get_item_by_id),
    path("users/<str:username>/", get_user_profile),
    path("articles/<slug:article_slug>/", get_article_by_slug),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
