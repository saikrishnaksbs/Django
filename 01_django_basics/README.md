# Topic 01: Django Basics & Routing

This module covers foundational Django web application features, including setting up standalone scripts, configuring routing, rendering HTML templates, and managing HTTP requests and JSON responses.

---

## Code Walkthrough

1. **[01_hello_world.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/01_django_basics/01_hello_world.py)**
   * Shows how to construct a minimal standalone Django app, config settings inline, register a root view, and run it with `execute_from_command_line`.
2. **[02_path_routing.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/01_django_basics/02_path_routing.py)**
   * Explains path routing matching rules and dynamic path type-converters (such as `<int:item_id>`).
3. **[03_views_and_templates.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/01_django_basics/03_views_and_templates.py)**
   * Covers function-based views (FBVs) and rendering templates using custom context dictionary mappings.
4. **[04_request_response.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/01_django_basics/04_request_response.py)**
   * Explains extracting parameters from GET/POST, decoding request bodies, and returning structured JSON payloads using `JsonResponse`.
