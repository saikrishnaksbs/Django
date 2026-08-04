# Topic 02: Django Models & ORM

This module covers Django's Object Relational Mapper (ORM), explaining how to declare model schemas, query databases using Django QuerySets, and configure relationships between tables.

---

## Code Walkthrough

1. **[01_model_declaration.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/02_django_models_and_orm/01_model_declaration.py)**
   * Shows how to configure Django to use an in-memory SQLite database, declare models with common field types, run structural tables compilation, and insert mock objects.
2. **[02_orm_queries.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/02_django_models_and_orm/02_orm_queries.py)**
   * Covers database CRUD queries: creating instances, fetching records using `.all()`, `.get()`, filtering with field lookups (e.g. `__contains`, `__gte`), and performing updates and deletes.
3. **[03_model_relationships.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/02_django_models_and_orm/03_model_relationships.py)**
   * Demonstrates One-to-Many (`ForeignKey`), Many-to-Many (`ManyToManyField`), and One-to-One (`OneToOneField`) schemas and how to perform related-lookup queries.

---

## How Standalone Django ORM Works
To use Django models inside a single script, we configure an in-memory database:
```python
settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    },
    INSTALLED_APPS=[__name__], # Register this script module itself as an app
)
```
After configuring, we run `django.setup()` and call:
```python
from django.core.management import call_command
# This automatically constructs SQLite database schema tables on the fly
call_command('migrate', run_syncdb=True)
```
This enables running a complete, sandbox database instance inside a single self-contained script!
