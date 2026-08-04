# Django & Django REST Framework (DRF) Learning Curriculum

This workspace is a structured, hands-on tutorial for learning and mastering **Django** and **Django REST Framework (DRF)**. Every folder represents a core module, containing an explanatory `README.md` and fully runnable, standalone code examples.

---

## Directory Index

1. **[01_django_basics](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/01_django_basics)**
   * Standalone routing, FBVs, Request/Response logic, custom query parameters, and templates.
2. **[02_django_models_and_orm](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/02_django_models_and_orm)**
   * Declaring Django Models, fields, CRUD operations via Django ORM, and database relationships (One-to-Many, Many-to-Many).
3. **[03_django_forms_and_admin](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/03_django_forms_and_admin)**
   * Declarative Forms, validation logic, and registering components with the django admin dashboard.
4. **[04_drf_basics](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/04_drf_basics)**
   * Initializing DRF, `@api_view`, and custom serializers to clean/map incoming payload models.
5. **[05_drf_class_views](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/05_drf_class_views)**
   * Class-based views (`APIView`), Generic Views (`ListCreateAPIView`), and `ModelViewSet` routing.
6. **[06_drf_authentication_and_permissions](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/06_drf_authentication_and_permissions)**
   * built-in token header validation and configuring permissions (custom and built-in).
7. **[07_drf_filtering_and_pagination](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/07_drf_filtering_and_pagination)**
   * Pagination limits, ordering, and field filtering search parameters.
8. **[08_django_middleware_and_signals](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/08_django_middleware_and_signals)**
   * Intercepting request hooks with Custom HTTP middleware and subscribing to ORM DB model events (Signals).
9. **[09_django_testing](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/09_django_testing)**
   * Testing endpoints using Django's `Client` and DRF's `APIClient` suites.

---

## How to Run the Code

To run any of the standalone files, you must first install the dependencies:

```bash
pip install django djangorestframework django-filter pytest pytest-django httpx
```

Since these files are written using Django's programmatically configured settings, you do not need to construct separate configuration projects! Simply run any script directly:

```bash
python3 <folder_name>/<file_name>.py runserver
```

For example, to run the Django Hello World example:
```bash
python3 01_django_basics/01_hello_world.py runserver
```
You can then open [http://127.0.0.1:8000](http://127.0.0.1:8000).
