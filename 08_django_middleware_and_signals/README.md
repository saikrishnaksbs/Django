# Topic 08: Middleware & Signals

This module covers custom middleware pipelines and Django's event framework (Signals), explaining how to hook execution steps and intercept model actions.

---

## Code Walkthrough

1. **[01_custom_middleware.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/08_django_middleware_and_signals/01_custom_middleware.py)**
   * Shows how to build a custom class-based HTTP middleware that calculates latency diagnostics and prints logs for every request.
2. **[02_django_signals.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/08_django_middleware_and_signals/02_django_signals.py)**
   * Demonstrates connecting signal listeners (`pre_save`, `post_save`) to execute side effects (like sending notifications or setting defaults) whenever database rows change.

---

## Signals vs Middleware

* **Middleware** operates at the HTTP boundary, checking headers, cookies, and HTTP request routing parameters.
* **Signals** operate at the ORM model level, responding to database activities (such as creating records or deleting related rows) regardless of where that change is triggered (e.g., from an API call, celery worker, or django admin panel).
