"""
DJANGO FORMS AND MODELFORMS VALIDATION
======================================
This script demonstrates how to define Forms and ModelForms,
handle validation errors, and clean submitted values.
"""

import sys
import django
from django.conf import settings
from django.db import models
from django import forms
from django.urls import path
from django.http import HttpResponse, JsonResponse
from django.template import Template, Context
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt

if not settings.configured:
    settings.configure(
        DEBUG=True,
        SECRET_KEY="temporary-secret-key-for-standalone-dev",
        INSTALLED_APPS=["__main__"],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
            }
        },
        TEMPLATES=[{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
        }]
    )
    django.setup()

# 1. Define target ORM Model
class Member(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField(blank=True)

    class Meta:
        app_label = "__main__"

# 2. Define ModelForm
# ModelForm links directly to a model class and generates fields automatically.
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["fullname", "email", "bio"]
        
    # Custom validation for 'fullname' field
    def clean_fullname(self):
        fullname = self.cleaned_data.get("fullname")
        if len(fullname) < 3:
            raise forms.ValidationError("Fullname must be at least 3 characters long.")
        return fullname

# 3. Simple Form HTML template
HTML_FORM_TEMPLATE = """
<html>
    <body>
        <h2>Register Member</h2>
        {% if errors %}
            <div style="color: red;">
                <strong>Please correct the following errors:</strong>
                {{ errors }}
            </div>
        {% endif %}
        
        <form method="POST" action="">
            <table>
                {{ form.as_table }}
            </table>
            <button type="submit">Submit Registration</button>
        </form>
    </body>
</html>
"""

# 4. Form handling View controller
@csrf_exempt
def register_member_view(request):
    errors = None
    if request.method == "POST":
        # Bind POST values to the form
        form = MemberForm(request.POST)
        if form.is_valid():
            # If valid, save the record to SQLite and return a success JSON response
            member = form.save()
            return JsonResponse({
                "status": "success",
                "member_id": member.id,
                "fullname": member.fullname
            })
        else:
            errors = form.errors.as_json()
    else:
        # Instantiate an empty form for GET
        form = MemberForm()

    # Render HTML page containing the form fields
    template = Template(HTML_FORM_TEMPLATE)
    context = Context({"form": form, "errors": errors})
    return HttpResponse(template.render(context))

urlpatterns = [
    path("", register_member_view),
]

if __name__ == "__main__":
    call_command("migrate", run_syncdb=True, verbosity=0)
    execute_from_command_line(sys.argv)
