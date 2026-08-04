# Topic 04: DRF Basics & Serializers

This module introduces **Django REST Framework (DRF)**, explaining how to write RESTful endpoint handlers, construct serializers to parse incoming payloads, and convert query records to JSON.

---

## Code Walkthrough

1. **[01_drf_hello_world.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/04_drf_basics/01_drf_hello_world.py)**
   * Demonstrates registering DRF in Django settings, writing an endpoint function using the `@api_view` wrapper decorator, and returning structured DRF `Response` objects.
2. **[02_drf_serializers.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/04_drf_basics/02_drf_serializers.py)**
   * Shows how to declare DRF `Serializer` and `ModelSerializer` classes. Teaches validation bounds, transforming fields (deserialization), and formatting databases states.

---

## What is a Serializer?

Web APIs receive and transmit strings/bytes over networks, but Django uses complex Python model instances. A **Serializer** behaves as the bridge:
* **Serialization**: Python object/QuerySet -> Native python dict -> JSON string.
* **Deserialization (Validation)**: Request payload JSON -> Python dict (validated via serializer fields) -> Python/ORM object.
