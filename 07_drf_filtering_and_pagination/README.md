# Topic 07: Filtering & Pagination

This module details how to manage large database datasets by configuring API search, filters, ordering criteria, and paging responses in Django REST Framework.

---

## Code Walkthrough

1. **[01_pagination.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/07_drf_filtering_and_pagination/01_pagination.py)**
   * Shows how to configure and override `PageNumberPagination` and `LimitOffsetPagination` parameters on generic views.
2. **[02_filtering_searching.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/07_drf_filtering_and_pagination/02_filtering_searching.py)**
   * Covers setting up text query searching (`SearchFilter`), field sorting (`OrderingFilter`), and integrating `django-filter` to match attributes dynamically.

---

## Why use Filtering & Pagination?

Returning thousands of rows on a single database query is inefficient:
* **Pagination**: Splits payloads into smaller pages (e.g. `next` / `previous` pages URLs).
* **Filtering**: Restricts outputs based on criteria (e.g. `category=electronics`).
* **Searching**: Matches text values across multiple columns (e.g. `?search=macbook`).
