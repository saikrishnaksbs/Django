"""
DJANGO ADMIN INTERFACE REGISTRATION
==================================
This script demonstrates how to register models with Django's Admin portal
and customize the administrative display tables.
"""

import sys
import django
from django.conf import settings
from django.db import models
from django.contrib import admin
from django.urls import path
from django.core.management import execute_from_command_line, call_command

# 1. Configure a full settings suite to support Admin & Authentication middleware
if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        INSTALLED_APPS=[
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.messages",
            "__main__",
        ],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "django_admin_demo.db", # Uses a persistent file to let the user log in
            }
        },
        MIDDLEWARE=[
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ],
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        }]
    )
    django.setup()

# 2. Define Model to manage
class Article(models.Model):
    title = models.CharField(max_length=200)
    author_name = models.CharField(max_length=100)
    content = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "__main__"

    def __str__(self):
        return self.title

# 3. Customizing the ModelAdmin class
# This shapes how the Article model is listed and edited in the admin UI.
class ArticleAdmin(admin.ModelAdmin):
    # Columns shown on the listing page
    list_display = ("title", "author_name", "is_published", "created_at")
    # Filters sidebar
    list_filter = ("is_published", "created_at")
    # Search bar input fields
    search_fields = ("title", "content")
    # Editable fields directly from list page
    list_editable = ("is_published",)

# 4. Register model with the admin site
admin.site.register(Article, ArticleAdmin)

# 5. Admin site routing
urlpatterns = [
    path("admin/", admin.site.urls),
]

if __name__ == "__main__":
    # Create the persistent DB schema
    call_command("migrate", verbosity=0)
    
    # Check if a superuser already exists; if not, print instructions to create one
    from django.contrib.auth.models import User
    if not User.objects.filter(is_superuser=True).exists():
        print("[ADMIN] No superuser detected. To create one, run:")
        print("python3 03_django_forms_and_admin/02_admin_site.py createsuperuser")
        print("-" * 50)
        
    execute_from_command_line(sys.argv)
