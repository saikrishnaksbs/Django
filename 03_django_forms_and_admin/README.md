# Topic 03: Django Forms & Admin

This module introduces Django's Form validation subsystems and demonstrates registering ORM database models into the built-in administration dashboard.

---

## Code Walkthrough

1. **[01_django_forms.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/03_django_forms_and_admin/01_django_forms.py)**
   * Shows how to declare standard HTTP validation schemes using `forms.Form` and `forms.ModelForm`. Explains validation hooks (like `clean_fieldname()` or `.is_valid()`).
2. **[02_admin_site.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/03_django_forms_and_admin/02_admin_site.py)**
   * Outlines how the Django admin portal auto-discovers and registers models to provide a customizable management dashboard.

---

## Django Forms System
Django Forms do two jobs:
* **HTML Generation**: Forms render clean HTML inputs automatically (`form.as_p`, `form.as_table`).
* **Data Sanitization**: Forms inspect incoming dictionary parameters, verify correct types, and save sanitized data inside `form.cleaned_data`.
