"""
HTTP REQUESTS AND JSON RESPONSES
================================
This script demonstrates how to parse incoming GET query parameters, POST forms,
JSON payloads, and return JSON responses using Django's `JsonResponse`.
"""

import json
import sys
from django.conf import settings
from django.urls import path
from django.http import JsonResponse, HttpResponseNotAllowed
from django.core.management import execute_from_command_line
from django.views.decorators.csrf import csrf_exempt

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
    )

# 1. Processing GET Query Parameters (?search=django&limit=10)
def search_view(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
        
    # Read query parameters from request.GET
    search_query = request.GET.get("search", "")
    limit = request.GET.get("limit", 10)
    
    return JsonResponse({
        "status": "success",
        "search_query": search_query,
        "limit": int(limit),
    })

# 2. Processing JSON POST payloads
# We use @csrf_exempt decorator to bypass CSRF token verification for testing.
@csrf_exempt
def create_product_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
        
    try:
        # Load and parse raw request body from request.body JSON string
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
    product_name = data.get("name", "Unknown")
    price = data.get("price", 0.0)
    
    return JsonResponse({
        "message": "Product created successfully",
        "product": {
            "name": product_name,
            "price": price
        }
    }, status=201)

urlpatterns = [
    path("search/", search_view),
    path("products/", create_product_view),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
