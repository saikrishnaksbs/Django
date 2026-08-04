# Topic 09: Testing & Mocking

This module teaches you how to write standard Django tests using the built-in test runners, and how to verify JSON REST API responses using DRF's custom `APIClient` classes.

---

## Code Walkthrough

1. **[01_django_test_client.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/09_django_testing/01_django_test_client.py)**
   * Shows how to inherit from Django's `SimpleTestCase` / `TestCase` and use `self.client` to execute GET/POST test assertions against view routes.
2. **[02_drf_apiclient.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/09_django_testing/02_drf_apiclient.py)**
   * Details using DRF's `APIClient` to check REST status codes, send payload dicts as JSON, and mock permissions boundaries.

---

## How to execute tests
You can run testing suites by running `pytest` directly:
```bash
pytest 09_django_testing/01_django_test_client.py
pytest 09_django_testing/02_drf_apiclient.py
```
Or utilizing Django's test runner:
```bash
python3 -m unittest 09_django_testing/01_django_test_client.py
```
Using DRF's APIClient simplifies formatting because it supports direct python dictionaries in requests, mapping them to application endpoints.
