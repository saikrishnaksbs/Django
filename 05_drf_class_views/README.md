# Topic 05: DRF Class-Based Views (CBVs)

This module explores class-based API views inside Django REST Framework, detailing code reuse hierarchies from manual `APIView` overrides up to automatic CRUD `ModelViewSet` routers.

---

## Code Walkthrough

1. **[01_apiview.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/05_drf_class_views/01_apiview.py)**
   * Shows how to inherit from `APIView` and override `get()`, `post()`, `put()`, and `delete()` methods.
2. **[02_generic_views.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/05_drf_class_views/02_generic_views.py)**
   * Covers using standard concrete views (`ListCreateAPIView` and `RetrieveUpdateDestroyAPIView`) which wrap common database mixins.
3. **[03_viewsets.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/05_drf_class_views/03_viewsets.py)**
   * Explains `ModelViewSet` layouts that combine listing, detail, creating, updating, and deleting routes into one class, automatically mapped using `DefaultRouter`.

---

## View Hierarchy in DRF

```
      ┌───────────┐
      │  APIView  │   <-- Complete flexibility, manual CRUD methods
      └─────┬─────┘
            ▼
 ┌─────────────────────┐
 │    GenericAPIView   │  <-- Combines serializers + querysets
 └──────────┬──────────┘
            ▼
┌───────────────────────┐
│     Generic Views     │ <-- Concrete views (e.g. ListCreateAPIView)
└───────────┬───────────┘
            ▼
     ┌─────────────┐
     │   ViewSet   │   <-- Action methods (list, retrieve, create...)
     └─────────────┘
```
Using ViewSets coupled with Routers isolates routing tables from logic, enforcing a clean API architecture.
