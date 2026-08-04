# Topic 06: Authentication & Permissions

This module details how to secure REST APIs in DRF using built-in Token schemes and configure request filtering permissions.

---

## Code Walkthrough

1. **[01_token_auth.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/06_drf_authentication_and_permissions/01_token_auth.py)**
   * Shows how to register and configure DRF's `TokenAuthentication` backend. Demonstrates generating tokens and passing them inside request HTTP headers (`Authorization: Token <token_key>`).
2. **[02_permission_classes.py](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/06_drf_authentication_and_permissions/02_permission_classes.py)**
   * Covers assigning built-in guards (`IsAuthenticated`, `IsAdminUser`) and constructing custom verification permissions.

---

## DRF Auth Pipeline
When a request hits DRF, it processes two scopes:
1. **Authentication**: Identifies the user profile (sets `request.user` and `request.auth`).
2. **Permissions**: Checks whether the identified user is allowed to access the view.
