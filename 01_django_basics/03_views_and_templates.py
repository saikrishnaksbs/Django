"""
VIEWS AND TEMPLATE RENDERING
============================
This script demonstrates Django's template engine.
We compile and render inline templates using the `Template` and `Context` classes.
"""

import sys
from django.conf import settings
from django.urls import path
from django.http import HttpResponse
from django.template import Template, Context
from django.core.management import execute_from_command_line

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        # Configure django templates engine settings
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
        }]
    )

# 1. HTML template using Django Template Syntax (variables, loops, conditionals)
TEMPLATE_STRING = """
<html>
    <head><title>Django Templates</title></head>
    <body>
        <h1>Welcome, {{ user_name|upper }}!</h1>
        {% if is_premium %}
            <p style="color: gold;">Premium subscriber content enabled.</p>
        {% else %}
            <p>Standard Member Account.</p>
        {% endif %}
        
        <h3>Current Course Topics:</h3>
        <ul>
            {% for topic in topics %}
                <li>{{ forloop.counter }}. {{ topic }}</li>
            {% empty %}
                <li>No topics listed.</li>
            {% endfor %}
        </ul>
    </body>
</html>
"""

def template_view(request):
    # Construct a Django Template instance
    template = Template(TEMPLATE_STRING)
    
    # Define variables inside the template context
    context = Context({
        "user_name": "saikrishna",
        "is_premium": True,
        "topics": ["Django Routing", "Django Views", "Template Engines", "ORM & Database Access"],
    })
    
    # Render and return
    return HttpResponse(template.render(context))

urlpatterns = [
    path("", template_view),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
