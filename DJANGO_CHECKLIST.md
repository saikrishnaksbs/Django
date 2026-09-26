# Master Django & Django REST Framework (DRF) Revision Checklist (Hierarchical Tree with Diagnostics)

> **Target Role**: Senior Backend Engineer / SDE-2 (Django, Django REST Framework, High-Concurrency Web Applications)  
> **Source Directory**: [/Users/saikrishnakuchimanchi/Downloads/Test/Django/](file:///Users/saikrishnakuchimanchi/Downloads/Test/Django/)  
> **Format**: 16 Master Topics with 2-Level Nested Active Recall Trees (`  - |__ **Category**` -> `      - |__ Details & Traps`).  
> **How to Revise**:
> 1. Open this file in **VS Code Markdown Preview** (`Cmd + K, V`) to view the interactive checkboxes and hierarchical tree branches.
> 2. Track your passes with the checkboxes (`- [ ]`) across Django ORM, Serializers, ViewSets, Middleware, Signals, and Async Django.

---

## 📊 High-Level Curriculum Dashboard

- [ ] **PART I: CORE DJANGO FRAMEWORK & ORM** (Topics 1 to 6)
- [ ] **PART II: DJANGO REST FRAMEWORK (DRF) ARCHITECTURE** (Topics 7 to 12)
- [ ] **PART III: MIDDLEWARE, SIGNALS, TESTING & PRODUCTION** (Topics 13 to 16)

---

### [ ] Topic 1. Django Architecture, Request-Response Lifecycle & Routing

- [ ] **Box 1: MVT Architecture & WSGI/ASGI Pipeline**
  - |__ **MVT Pattern**
      - |__ Model (Data access & ORM), View (Business logic & Controller), Template (Presentation)
      - |__ WSGI entry point (`wsgi.py`) vs ASGI entry point (`asgi.py`)
      - |__ Request-response lifecycle: Web Server -> WSGI Handler -> Middleware -> URL Resolver -> View -> Template/JSON -> Response
  - |__ **URL Routing & Path Converters**
      - |__ `path()` and `re_path()`: String patterns vs regex routes
      - |__ Built-in path converters: `<int:id>`, `<str:slug>`, `<uuid:pk>`, `<path:subpath>`
      - |__ Namespace resolution: `include('app.urls', namespace='v1')` and `reverse('v1:user-detail')`

- [ ] **Box 2: Function-Based Views (FBVs) & HTTP Objects**
  - |__ **HttpRequest & HttpResponse**
      - |__ `HttpRequest`: `request.method`, `request.GET` (QueryDict), `request.POST`, `request.headers`, `request.user`
      - |__ Response types: `HttpResponse`, `JsonResponse(data, safe=False)`, `HttpResponseRedirect`, `Http404`
      - |__ View decorators: `@require_http_methods(["GET", "POST"])`, `@login_required`

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Routing Traps**
      - |__ Trap 1: `request.GET['key']` raises `MultiValueDictKeyError` if key is missing (always use `request.GET.get('key')`)
      - |__ Trap 2: Hardcoding URL strings instead of using `reverse()` or `{% url %}` breaking upon path refactoring

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **URL Resolver Engine**
      - |__ `URLResolver.resolve()` matching URL patterns against loaded regex trees and extracting keyword arguments

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **Django MVT vs Standard MVC**
      - |__ Django View acts as the Controller in traditional MVC, while Template acts as the View

---

### [ ] Topic 2. Django Models, Fields & Database Migrations

- [ ] **Box 1: Declarative Model Definition**
  - |__ **Field Types & Attributes**
      - |__ Basic fields: `CharField(max_length=...)`, `IntegerField()`, `BooleanField()`, `DateTimeField(auto_now_add=True)`
      - |__ Text & JSON: `TextField()`, `JSONField()`, `UUIDField(default=uuid.uuid4, editable=False)`
      - |__ Column constraints: `null=True` (database level) vs `blank=True` (form validation level)
      - |__ Meta options: `db_table`, `ordering`, `unique_together`, `indexes = [models.Index(fields=['email'])]`

- [ ] **Box 2: Migration Engine & Evolution**
  - |__ **Migration Workflow**
      - |__ `python manage.py makemigrations`: Inspects model changes and generates numbered migration files
      - |__ `python manage.py migrate`: Applies unapplied migrations against target database
      - |__ Migration tracking: `django_migrations` database table storing applied migration hashes
      - |__ Custom migrations: `migrations.RunPython(forward_func, reverse_func)` for data transformations

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Model & Migration Traps**
      - |__ Trap 1: Setting `null=True` on `CharField` or `TextField` causes two representations of empty values (`NULL` and `""`); use `blank=True` only
      - |__ Trap 2: Adding a non-nullable field without a default value to an existing populated table halts migrations

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Django Migration State Graph**
      - |__ Dependency graph resolving circular migration dependencies through topological ordering

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **null=True vs blank=True**
      - |__ null=True: Database column level (stores NULL in SQL)
      - |__ blank=True: Form & Serializer validation level (field is not required in inputs)

---

### [ ] Topic 3. Django ORM Queries, QuerySets & Lazy Evaluation

- [ ] **Box 1: QuerySet Architecture & Lazy Evaluation**
  - |__ **Lazy Loading Mechanics**
      - |__ QuerySets are lazy: Creating `qs = User.objects.filter(is_active=True)` does NOT hit the database!
      - |__ Evaluation triggers: Iteration (`for x in qs`), Slicing with step, `len()`, `list()`, `bool(qs)`, caching in `qs._result_cache`
      - |__ Query chaining: Method calls return clone of QuerySet without executing SQL

- [ ] **Box 2: Filtering, Lookups & Complex Logic (Q & F Objects)**
  - |__ **Field Lookups & Logic**
      - |__ Exact & Partial: `field__exact`, `field__iexact`, `field__contains`, `field__icontains`, `field__startswith`
      - |__ Ranges & Nulls: `field__gt`, `field__gte`, `field__lt`, `field__in=[1, 2]`, `field__isnull=True`
      - |__ Q Objects: Complex logical OR, AND, and NOT queries (`Q(role='admin') | Q(score__gte=90)`, `~Q(status='banned')`)
      - |__ F Expressions: Database-level attribute references (`F('stock') - 1`) avoiding race conditions in concurrent updates

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **QuerySet Traps**
      - |__ Trap 1: Checking QuerySet existence using `if len(qs) > 0:` loads all records into memory; use `if qs.exists():`
      - |__ Trap 2: Counting records with `len(qs)` instead of `qs.count()` (which executes `SELECT COUNT(*)`)
      - |__ Trap 3: Race condition when updating balance: `obj.balance += 10; obj.save()` (use `F('balance') + 10`)

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **SQLCompiler & QuerySet Cache**
      - |__ How `QuerySet._result_cache` stores hydrated model instances on first evaluation to prevent repeat queries

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **qs.exists() vs qs.count() vs bool(qs)**
      - |__ exists(): Emits `SELECT 1 ... LIMIT 1` (fastest existence check)
      - |__ count(): Emits `SELECT COUNT(*)` (fastest count calculation)
      - |__ bool(qs): Evaluates and caches full result set in memory

---

### [ ] Topic 4. Database Relationships, Joins & Optimization (N+1 Solution)

- [ ] **Box 1: Relationship Topologies**
  - |__ **Declaring Relations**
      - |__ One-to-Many: `models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='children')`
      - |__ One-to-One: `models.OneToOneField(Profile, on_delete=models.CASCADE)`
      - |__ Many-to-Many: `models.ManyToManyField(Tag, blank=True)` with optional `through='Membership'` intermediary model
      - |__ On-delete behaviors: `CASCADE`, `PROTECT`, `SET_NULL`, `SET_DEFAULT`, `DO_NOTHING`

- [ ] **Box 2: Solving N+1 Queries: select_related vs prefetch_related**
  - |__ **Eager Loading Strategies**
      - |__ `select_related('foreign_key')`: Performs SQL `INNER JOIN` or `LEFT OUTER JOIN` (for 1:1 and Single-parent FKs)
      - |__ `prefetch_related('many_to_many')`: Performs separate query with `WHERE id IN (...)` and joins in Python (for M:N and Reverse FKs)
      - |__ `Prefetch()` object: Customizing queryset of prefetched relationships (`Prefetch('orders', queryset=Order.objects.filter(is_paid=True))`)

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Relationship Traps**
      - |__ Trap 1: Using `select_related` on a ManyToMany relationship raises a TypeError (must use `prefetch_related`)
      - |__ Trap 2: Calling `.filter()` on an already prefetched related manager busts the cache and triggers a fresh SQL query!

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Prefetch Cache Hydration Engine**
      - |__ How Django's `prefetch_related_objects` parses foreign keys and attaches instances to `_prefetched_objects_cache`

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **select_related vs prefetch_related**
      - |__ select_related: 1 SQL query with JOIN; works only for single-valued relationships (ForeignKey, OneToOne)
      - |__ prefetch_related: 2 SQL queries (no JOIN); works for multi-valued relationships (ManyToMany, Reverse ForeignKey)

---

### [ ] Topic 5. Aggregations, Annotations & Transactions

- [ ] **Box 1: Aggregate vs Annotate**
  - |__ **Aggregations & Calculations**
      - |__ `aggregate()`: Terminal calculation reducing QuerySet to a dictionary (`Book.objects.aggregate(avg_price=Avg('price'))`)
      - |__ `annotate()`: Per-object calculation adding virtual fields to every row (`Author.objects.annotate(book_count=Count('book'))`)
      - |__ Complex expressions: `Coalesce()`, `Case()`, `When()` for conditional aggregations inside SQL

- [ ] **Box 2: Database Transactions & Concurrency Locks**
  - |__ **Transaction Management**
      - |__ Automatic transactions: `ATOMIC_REQUESTS = True` wrapping whole HTTP request in transaction
      - |__ Explicit transactions: `with transaction.atomic(): ...`
      - |__ Row-level locking: `select_for_update(nowait=False, skip_locked=False)` preventing lost updates in concurrent transactions
      - |__ Post-commit hooks: `transaction.on_commit(lambda: send_email.delay())` preventing race conditions with background tasks

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Transaction Traps**
      - |__ Trap 1: Dispatching Celery background task inside `transaction.atomic()` before commit: Worker runs before DB row is visible!
      - |__ Trap 2: Combining `select_for_update()` without an enclosing `transaction.atomic()` block raises TransactionManagementError

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Atomic Context Manager (Savepoints)**
      - |__ How nested `transaction.atomic()` blocks translate into SQL `SAVEPOINT` and `ROLLBACK TO SAVEPOINT` directives

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **Optimistic Locking vs Pessimistic Locking**
      - |__ Optimistic: Version column check (`WHERE version = 1`), high throughput, retry logic needed
      - |__ Pessimistic (`select_for_update`): DB exclusive lock, prevents conflicts, blocks competing transactions

---

### [ ] Topic 6. Django Forms, Validation & Admin Dashboard

- [ ] **Box 1: Form Validation Protocol**
  - |__ **Forms & ModelForms**
      - |__ `forms.Form` vs `forms.ModelForm` (automatic field generation from Model)
      - |__ Validation lifecycle: `is_valid()` -> `clean_<field>()` -> `clean()` -> `cleaned_data` dictionary
      - |__ Raising `forms.ValidationError` for invalid inputs

- [ ] **Box 2: Django Admin Customization**
  - |__ **Admin Model Customization**
      - |__ `@admin.register(Book)`: Subclassing `admin.ModelAdmin`
      - |__ Dashboard configuration: `list_display`, `list_filter`, `search_fields`, `ordering`, `readonly_fields`
      - |__ Inline models: `admin.TabularInline` and `admin.StackedInline` for editing child models on parent page

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Admin Traps**
      - |__ Trap 1: N+1 queries in Django Admin: Omitting `list_select_related` on Admin models displaying foreign key columns
      - |__ Trap 2: Accessing `form.cleaned_data` before calling `form.is_valid()` raises AttributeError

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Form Data Cleaning Pipeline**
      - |__ Sequence of field `to_python()`, `validate()`, `run_validators()`, and form `clean()` methods

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **Form vs ModelForm**
      - |__ Form: Unbound to database, ideal for contact forms, searches, authentication
      - |__ ModelForm: Automatically synchronizes with database models, auto-generates fields

---

### [ ] Topic 7. DRF Basics: Serialization, Deserialization & @api_view

- [ ] **Box 1: Serializer Architecture**
  - |__ **Serialization & Deserialization**
      - |__ `serializers.Serializer` vs `serializers.ModelSerializer`
      - |__ Outgoing serialization: Model instance -> Serializer -> `serializer.data` (Python dict) -> JSON
      - |__ Incoming deserialization: Raw JSON -> `serializer = Serializer(data=...)` -> `is_valid()` -> `serializer.validated_data`
      - |__ Persistence: `serializer.save()` calling `create()` or `update()` methods

- [ ] **Box 2: Function-Based DRF Views (@api_view)**
  - |__ **API View Decorator**
      - |__ `@api_view(['GET', 'POST'])`: Transforms regular view into DRF `APIView`
      - |__ DRF `Request` wrapping Django request (provides `request.data` parsing JSON/form data and `request.query_params`)
      - |__ DRF `Response`: Content negotiation returning JSON or browsable API HTML

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Serializer Traps**
      - |__ Trap 1: Accessing `serializer.validated_data` before calling `serializer.is_valid()` raises AssertionError
      - |__ Trap 2: Modifying an existing instance without passing instance argument: `Serializer(data=...)` creates; `Serializer(instance, data=...)` updates

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **DRF Content Negotiation Engine**
      - |__ `DefaultContentNegotiator` inspecting `Accept` header to select renderer (JSONRenderer vs BrowsableAPIRenderer)

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **request.POST vs request.data**
      - |__ request.POST: Only parses form-encoded data (`application/x-www-form-urlencoded`)
      - |__ request.data: Parses JSON, multipart form data, YAML, custom media types transparently

---

### [ ] Topic 8. Serializer Validation, Nested Serializers & MethodFields

- [ ] **Box 1: Validation Hierarchy in DRF**
  - |__ **3-Tier Validation Structure**
      - |__ Field-level validator: `validate_<field_name>(self, value)`
      - |__ Object-level validator: `validate(self, attrs)` for cross-field validation rules
      - |__ External reusable validators: `validators=[UniqueValidator(queryset=...)]` in field definitions

- [ ] **Box 2: Nested Serializers & SerializerMethodField**
  - |__ **Relational Representation**
      - |__ Nested reading: `author = AuthorSerializer(read_only=True)`
      - |__ Dynamic computed fields: `full_name = serializers.SerializerMethodField()` with `get_full_name(self, obj)`
      - |__ Writable nested serializers: Overriding `create()` and `update()` to handle manual nested child creation

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Validation Traps**
      - |__ Trap 1: `SerializerMethodField` is read-only by default; assigning input data to it is silently ignored!
      - |__ Trap 2: Writing into nested relationships without overriding `create()` raises NotImplementedError in DRF

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **to_internal_value() vs to_representation()**
      - |__ `to_internal_value()` validates input primitives into Python objects; `to_representation()` serializes Python objects to primitives

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **PrimaryKeyRelatedField vs Nested Serializer**
      - |__ PrimaryKeyRelatedField: Lightweight, passes integer ID, ideal for write operations
      - |__ Nested Serializer: Rich nested object representation, higher payload size, ideal for read operations

---

### [ ] Topic 9. Class-Based Views: APIView, Generic Views & ViewSets

- [ ] **Box 1: APIView & GenericAPIView**
  - |__ **Class Hierarchy**
      - |__ `APIView`: Lowest-level CBV, implements explicit `get()`, `post()`, `put()`, `delete()` methods
      - |__ `GenericAPIView`: Adds `queryset` and `serializer_class` attributes, `get_object()`, and `get_queryset()`
      - |__ Mixins: `ListModelMixin`, `CreateModelMixin`, `RetrieveModelMixin`, `UpdateModelMixin`, `DestroyModelMixin`

- [ ] **Box 2: Concrete Generic Views & ViewSets**
  - |__ **High-Level Abstractions**
      - |__ Concrete Views: `ListCreateAPIView`, `RetrieveUpdateDestroyAPIView`
      - |__ `ModelViewSet`: Implements complete CRUD actions (`list`, `create`, `retrieve`, `update`, `partial_update`, `destroy`)
      - |__ Extra actions: `@action(detail=True, methods=['post'])` for custom sub-endpoints (e.g. `/users/1/set_password/`)
      - |__ DRF Routers: `DefaultRouter()` automatically generating RESTful URL configuration for ViewSets

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **View Traps**
      - |__ Trap 1: Overriding `get_queryset()` but evaluating it at class definition time: `queryset = Model.objects.all()` evaluates once on startup!
      - |__ Trap 2: Forgetting `lookup_field = 'slug'` when using slug-based URLs in ViewSets defaults to searching by integer primary key

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **ViewSet Action Dispatcher**
      - |__ How `ViewSet.as_view({'get': 'list', 'post': 'create'})` maps HTTP methods to action handler methods

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **APIView vs GenericAPIView vs ModelViewSet**
      - |__ APIView: Complete manual control over every method, highest boilerplate
      - |__ GenericAPIView + Mixins: Semi-automated, standard patterns, good flexibility
      - |__ ModelViewSet: Maximum DRY automation, complete RESTful CRUD in 5 lines of code

---

### [ ] Topic 10. DRF Authentication & Permission Systems

- [ ] **Box 1: Authentication Schemes**
  - |__ **Authentication Protocols**
      - |__ `SessionAuthentication`: Cookie-based session validation for browser clients (requires CSRF tokens)
      - |__ `TokenAuthentication`: Built-in database token (`Authorization: Token <key>`)
      - |__ JWT Authentication: `djangorestframework-simplejwt` with Access and Refresh tokens
      - |__ Setting auth schemes: Globally in `REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES']` or per-view via `authentication_classes`

- [ ] **Box 2: Permissions Architecture**
  - |__ **Permission Classes**
      - |__ Built-in permissions: `AllowAny`, `IsAuthenticated`, `IsAdminUser`, `IsAuthenticatedOrReadOnly`
      - |__ Custom permissions: Subclassing `BasePermission` and implementing `has_permission()` (view-level) and `has_object_permission()` (row-level)
      - |__ Bitwise composition: `permission_classes = [IsAuthenticated & (IsOwner | IsAdmin)]`

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Security Traps**
      - |__ Trap 1: `has_object_permission()` is NEVER called on `list` or `create` requests (only called on `retrieve`, `update`, `destroy`)
      - |__ Trap 2: CSRF validation failure when using `SessionAuthentication` in Postman / API clients without CSRF token header

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Permission Checking Sequence**
      - |__ `check_permissions(request)` executed before view action; `check_object_permissions(request, obj)` called manually or by `get_object()`

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **Authentication vs Permission**
      - |__ Authentication: Answers "Who are you?" (attaches `request.user` and `request.auth`)
      - |__ Permission: Answers "Are you allowed to perform this action?" (returns HTTP 401 Unauthorized or 403 Forbidden)

---

### [ ] Topic 11. Filtering, Searching, Ordering & Pagination

- [ ] **Box 1: Filtering & Search (django-filter)**
  - |__ **Filter Backends**
      - |__ `DjangoFilterBackend`: Declarative filtering via `filterset_fields = ['category', 'status']` or custom `FilterSet`
      - |__ `filters.SearchFilter`: Full-text substring search across `search_fields = ['title', 'author__name']`
      - |__ `filters.OrderingFilter`: Query parameter ordering via `ordering_fields = ['price', 'created_at']`

- [ ] **Box 2: Pagination Strategies**
  - |__ **Pagination Classes**
      - |__ `PageNumberPagination`: Traditional page navigation (`?page=2&page_size=20`)
      - |__ `LimitOffsetPagination`: SQL-native pagination (`?limit=20&offset=40`)
      - |__ `CursorPagination`: Keyshot-based opaque token pagination (`?cursor=...`) guaranteeing consistent pagination during high-frequency insertions

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Pagination Traps**
      - |__ Trap 1: Using `PageNumberPagination` on high-offset queries (e.g. `?page=10000`) causes slow `OFFSET` scans in PostgreSQL (use `CursorPagination`)
      - |__ Trap 2: Using `CursorPagination` without specifying an unambiguous unique `ordering` (e.g. `ordering = '-created_at'`) causes erratic paginated pages

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Cursor Pagination Token Encoding**
      - |__ Base64 encoding of sort key values and offsets preventing page drift during concurrent writes

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **PageNumber vs LimitOffset vs CursorPagination**
      - |__ PageNumber: User-friendly for UI page numbers, slow at deep offsets
      - |__ LimitOffset: Flexible API client limits, slow at deep offsets
      - |__ Cursor: Constant-time O(1) performance at infinite depth, prevents duplicate items on live feeds, no direct page jumping

---

### [ ] Topic 12. DRF Exception Handling, Throttling & Caching

- [ ] **Box 1: Custom Exception Handlers**
  - |__ **Exception Interception**
      - |__ Default handler: `rest_framework.views.exception_handler` handling DRF `APIException` subclasses
      - |__ Custom exception handler: Intercepting custom exceptions, logging tracebacks, and formatting uniform JSON `{status, error, code}`

- [ ] **Box 2: Throttling & Caching**
  - |__ **Rate Limiting & Performance**
      - |__ Throttling classes: `AnonRateThrottle` (IP-based) and `UserRateThrottle` (user-based) with rates (e.g. `'100/day'`, `'10/minute'`)
      - |__ Caching views: `@method_decorator(cache_page(60 * 15))` caching view response in Redis
      - |__ Conditional requests: `ETag` and `Last-Modified` headers via `condition()` decorator

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Throttling Traps**
      - |__ Trap 1: Running `AnonRateThrottle` behind a reverse proxy (e.g. NGINX) without configuring `NUM_PROXIES` rates all users under NGINX's single IP!

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Sliding Window / Leaky Bucket Throttling**
      - |__ How DRF throttle classes use Redis cache timestamps to calculate request rates over rolling time windows

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **Throttling vs Permissions**
      - |__ Throttling: Enforces rate limits (returns HTTP 429 Too Many Requests)
      - |__ Permissions: Enforces authorization access (returns HTTP 403 Forbidden)

---

### [ ] Topic 13. Django Middleware & The Request Hook Pipeline

- [ ] **Box 1: Middleware Architecture**
  - |__ **Middleware Contract**
      - |__ Callable taking `get_response`: `class SimpleMiddleware: def __init__(self, get_response): ...`
      - |__ Request & Response hooks: Code before `get_response(request)` runs on request entry; code after runs on response exit
      - |__ Special hook methods: `process_view()`, `process_exception()`, `process_template_response()`

- [ ] **Box 2: Built-in Middlewares & Ordering**
  - |__ **Security & Core Middlewares**
      - |__ `SecurityMiddleware`: HTTPS redirects, HSTS, X-Content-Type-Options
      - |__ `SessionMiddleware` & `AuthenticationMiddleware`: Populates `request.session` and `request.user`
      - |__ `CsrfViewMiddleware`: Enforces CSRF tokens on state-changing requests (POST, PUT, DELETE)
      - |__ Critical rule: Middleware execution order matters! AuthenticationMiddleware MUST be after SessionMiddleware

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Middleware Traps**
      - |__ Trap 1: Placing custom middleware that accesses `request.user` before `AuthenticationMiddleware` in `settings.MIDDLEWARE` causes AttributeError
      - |__ Trap 2: Short-circuiting middleware by returning an `HttpResponse` directly skips all remaining inner middlewares and view execution

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Middleware Onion Architecture**
      - |__ Nested recursive wrapper functions constructed at server startup in `BaseHandler.load_middleware()`

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **process_view vs process_request**
      - |__ Code in `__call__` before `get_response`: Runs before URL resolution (unaware of which view will run)
      - |__ `process_view`: Runs after URL resolution (has direct access to view function and its args)

---

### [ ] Topic 14. Django Signals: Decoupling & Event Handling

- [ ] **Box 1: Built-in Model Signals**
  - |__ **Signal Types & Dispatch**
      - |__ `pre_save` & `post_save`: Dispatched before and after `model.save()` (provides `instance` and `created: bool`)
      - |__ `pre_delete` & `post_delete`: Dispatched around model deletion
      - |__ `m2m_changed`: Dispatched when modifying ManyToMany relationships
      - |__ Signal receivers: `@receiver(post_save, sender=User)` in `signals.py` registered in `apps.py` `ready()` method

- [ ] **Box 2: Custom Signals & Signal Trade-offs**
  - |__ **Event-Driven Patterns**
      - |__ Defining custom signals: `order_paid = django.dispatch.Signal()`
      - |__ Sending signals: `order_paid.send(sender=self.__class__, order=self)`
      - |__ Anti-pattern warning: Overusing signals creates hidden control flow and tight implicit coupling

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Signals Traps**
      - |__ Trap 1: Signals are SYNCHRONOUS: Heavy processing inside a `post_save` receiver blocks the user's HTTP response!
      - |__ Trap 2: Bulk operations (`bulk_create()`, `bulk_update()`, `QuerySet.update()`, `QuerySet.delete()`) DO NOT trigger signals!
      - |__ Trap 3: Calling `instance.save()` inside a `post_save` receiver without recursion guards causes an infinite loop

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Signal Dispatcher Implementation**
      - |__ Weak reference tracking (`weakref`) of connected receiver functions preventing memory leaks

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **Signals vs Overriding save() method**
      - |__ Overriding `save()`: Direct, explicit, readable, easily debugged, best for model-local state
      - |__ Signals: Decouples third-party apps, best when multiple independent modules listen to one event

---

### [ ] Topic 15. Testing Django & DRF Applications

- [ ] **Box 1: Django Test Suite & Test Client**
  - |__ **Testing Foundations**
      - |__ `TestCase`: Runs tests inside database transaction rollbacks for speed
      - |__ Django `Client`: Simulates browser requests (`client.get('/url/')`, `client.post()`)
      - |__ Fixtures & Factory Boy: Generating mock data (`baker.make(User)` or `UserFactory()`)

- [ ] **Box 2: DRF APIClient & APITestCase**
  - |__ **API Testing**
      - |__ `APITestCase` & `APIClient`: Direct testing of REST endpoints with JSON payloads (`client.post(url, data, format='json')`)
      - |__ Token authorization in tests: `client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)`
      - |__ Assertions: `assert response.status_code == status.HTTP_201_CREATED`

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Testing Traps**
      - |__ Trap 1: Using `TransactionTestCase` instead of `TestCase` when not testing transactions slows down test runs by 10x!
      - |__ Trap 2: Forgetting to mock external HTTP requests in tests causing CI flakiness and slow runs

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Django Test Runner Database Isolation**
      - |__ Automatic creation of temporary `test_` prefixed database destroyed after test execution

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **Django Client vs DRF APIClient**
      - |__ Django Client: Encodes form-data by default, requires manual JSON parsing
      - |__ DRF APIClient: Supports `format='json'`, handles DRF response status codes and headers natively

---

### [ ] Topic 16. Asynchronous Django, Channels & Production Deployment

- [ ] **Box 1: Async Views & Async ORM (Django 4.2+)**
  - |__ **Native Async Support**
      - |__ Async views: `async def my_view(request):` for non-blocking I/O
      - |__ Async ORM interfaces: `await User.objects.aget(id=1)`, `async for user in User.objects.filter():`
      - |__ Bridging sync/async: `sync_to_async` and `async_to_sync` helpers from `asgiref`

- [ ] **Box 2: Production WSGI/ASGI Architecture**
  - |__ **Production Deployment Stack**
      - |__ WSGI Servers: Gunicorn / uWSGI running synchronous Django workers
      - |__ ASGI Servers: Daphne / Uvicorn running Django Channels and async views
      - |__ Static files: `python manage.py collectstatic` served via NGINX or WhiteNoise
      - |__ Celery & Redis: Distributed asynchronous task queue for email delivery, exports, and heavy jobs

- [ ] **⚡ High-Yield Interview Traps & Pitfalls**
  - |__ **Async & Production Traps**
      - |__ Trap 1: Synchronous ORM calls inside `async def` views trigger `SynchronousOnlyOperation` exception!
      - |__ Trap 2: Running Django with `DEBUG = True` in production leaks all SQL queries, settings, and secrets into memory and crashes server

- [ ] **✍️ SDE-2 Deep-Dive Internals Frameworks**
  - |__ **Asgiref Thread Adaptation Layer**
      - |__ How Django routes synchronous code into thread pools when called from async contexts

- [ ] **⚖️ Master Comparative Matrix**
  - |__ **Gunicorn (WSGI) vs Uvicorn (ASGI)**
      - |__ Gunicorn: Robust synchronous production standard, mature, simple debugging
      - |__ Uvicorn / Daphne: Required for WebSockets (Django Channels), async views, server-sent events
