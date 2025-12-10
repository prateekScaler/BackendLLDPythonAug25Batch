# Django Views & URLs

## Views Overview

Views contain the logic for handling requests and returning responses. Django supports two types of views:
1. **Function-Based Views (FBV)**
2. **Class-Based Views (CBV)**

---

## Function-Based Views (FBV)

### Basic View
```python
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import User

def index(request):
    """Simple view returning HTML"""
    return HttpResponse("Hello, World!")

def user_list(request):
    """View with database query"""
    users = User.objects.all()
    return render(request, 'users/list.html', {'users': users})

def user_detail(request, user_id):
    """View with parameter"""
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/detail.html', {'user': user})

def api_users(request):
    """JSON API response"""
    users = list(User.objects.values('id', 'name', 'email'))
    return JsonResponse({'users': users})
```

### Handling Different HTTP Methods
```python
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def create_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        user = User.objects.create(name=name, email=email)
        return redirect('user-detail', user_id=user.id)

    return render(request, 'users/create.html')
```

### Handling Forms
```python
from django.shortcuts import render, redirect
from .forms import UserForm

def create_user_form(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-list')
    else:
        form = UserForm()

    return render(request, 'users/form.html', {'form': form})
```

---

## Class-Based Views (CBV)

### Basic CBV
```python
from django.views import View
from django.http import HttpResponse

class IndexView(View):
    def get(self, request):
        return HttpResponse("Hello from CBV!")

    def post(self, request):
        # Handle POST request
        return HttpResponse("POST request handled")
```

### Generic Views

#### ListView
```python
from django.views.generic import ListView
from .models import User

class UserListView(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        # Custom filtering
        queryset = super().get_queryset()
        return queryset.filter(is_active=True)

    def get_context_data(self, **kwargs):
        # Add extra context
        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        return context
```

#### DetailView
```python
from django.views.generic import DetailView

class UserDetailView(DetailView):
    model = User
    template_name = 'users/detail.html'
    context_object_name = 'user'

    # By default, expects 'pk' in URL
    # Can customize with slug_field and slug_url_kwarg
```

#### CreateView
```python
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

class UserCreateView(CreateView):
    model = User
    template_name = 'users/form.html'
    fields = ['name', 'email', 'age']
    success_url = reverse_lazy('user-list')

    def form_valid(self, form):
        # Custom logic before saving
        form.instance.created_by = self.request.user
        return super().form_valid(form)
```

#### UpdateView
```python
from django.views.generic.edit import UpdateView

class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/form.html'
    fields = ['name', 'email', 'age']
    success_url = reverse_lazy('user-list')
```

#### DeleteView
```python
from django.views.generic.edit import DeleteView

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/confirm_delete.html'
    success_url = reverse_lazy('user-list')
```

---

## URL Patterns

### Basic URL Routing
```python
from django.urls import path
from . import views

app_name = 'users'  # Namespace

urlpatterns = [
    # Function-based views
    path('', views.index, name='index'),
    path('users/', views.user_list, name='user-list'),
    path('users/<int:user_id>/', views.user_detail, name='user-detail'),

    # Class-based views
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user-update'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user-delete'),
]
```

### URL Parameters

```python
from django.urls import path

urlpatterns = [
    # Integer parameter
    path('users/<int:id>/', views.user_detail),

    # String parameter
    path('users/<str:username>/', views.user_by_username),

    # Slug parameter
    path('posts/<slug:slug>/', views.post_detail),

    # UUID parameter
    path('items/<uuid:item_id>/', views.item_detail),

    # Path parameter (matches any path including /)
    path('files/<path:file_path>/', views.serve_file),
]
```

### URL Converters
- `int` - Matches positive integers
- `str` - Matches any non-empty string (excluding `/`)
- `slug` - Matches slug strings (letters, numbers, hyphens, underscores)
- `uuid` - Matches UUID
- `path` - Matches any string including `/`

### include() for App URLs
```python
# Project urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('api/', include('api.urls')),
]
```

### Reverse URL Resolution
```python
from django.urls import reverse
from django.shortcuts import redirect

def my_view(request):
    # Reverse URL by name
    url = reverse('user-detail', kwargs={'user_id': 1})
    # Returns: /users/1/

    return redirect('user-list')
```

**In templates:**
```html
<a href="{% url 'user-detail' user_id=user.id %}">View User</a>
<a href="{% url 'users:user-list' %}">All Users</a>  <!-- With namespace -->
```

---

## Request & Response

### Request Object
```python
def my_view(request):
    # HTTP method
    if request.method == 'POST':
        pass

    # GET parameters: /users/?page=2&sort=name
    page = request.GET.get('page', 1)
    sort = request.GET.get('sort', 'id')

    # POST data
    name = request.POST.get('name')

    # Headers
    user_agent = request.META.get('HTTP_USER_AGENT')

    # User
    if request.user.is_authenticated:
        user = request.user

    # Files
    if request.FILES:
        uploaded_file = request.FILES['file']

    # Request path
    path = request.path  # /users/
    full_path = request.get_full_path()  # /users/?page=2

    # Check if AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
```

### Response Types
```python
from django.http import (
    HttpResponse, JsonResponse, FileResponse,
    HttpResponseRedirect, Http404
)
from django.shortcuts import render, redirect

def examples(request):
    # Simple text response
    return HttpResponse("Hello")

    # HTML response
    return HttpResponse("<h1>Hello</h1>", content_type="text/html")

    # JSON response
    return JsonResponse({'status': 'success', 'data': [1, 2, 3]})

    # Render template
    return render(request, 'template.html', {'key': 'value'})

    # Redirect
    return redirect('user-list')
    return HttpResponseRedirect('/users/')

    # 404 response
    raise Http404("User not found")

    # File response
    file = open('document.pdf', 'rb')
    return FileResponse(file, as_attachment=True, filename='download.pdf')
```

---

## Decorators

### Common View Decorators
```python
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, permission_required

# Require specific HTTP methods
@require_http_methods(["GET", "POST"])
def my_view(request):
    pass

@require_GET
def get_only_view(request):
    pass

@require_POST
def post_only_view(request):
    pass

# Require authentication
@login_required
def protected_view(request):
    pass

# Require specific permission
@permission_required('app.add_user')
def admin_view(request):
    pass

# Disable CSRF protection (use carefully!)
@csrf_exempt
def api_view(request):
    pass
```

### CBV with Decorators
```python
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Apply to single method
class MyView(View):
    @method_decorator(login_required)
    def get(self, request):
        pass

# Apply to entire class
@method_decorator(login_required, name='dispatch')
class ProtectedView(View):
    def get(self, request):
        pass
```

---

## Mixins for CBV

```python
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView

class UserListView(LoginRequiredMixin, ListView):
    model = User
    login_url = '/login/'  # Where to redirect if not logged in

class AdminUserListView(PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'
```

---

## Context Processors

Add global context available in all templates.

```python
# myapp/context_processors.py
def site_info(request):
    return {
        'site_name': 'My Site',
        'current_year': 2024,
    }

# settings.py
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                # ... default processors
                'myapp.context_processors.site_info',
            ],
        },
    },
]
```

---

## Middleware

Custom middleware for request/response processing.

```python
# myapp/middleware.py
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code executed before view
        print(f"Request: {request.path}")

        response = self.get_response(request)

        # Code executed after view
        print(f"Response status: {response.status_code}")

        return response

# settings.py
MIDDLEWARE = [
    # ... default middleware
    'myapp.middleware.CustomMiddleware',
]
```

---

## Best Practices

1. **Use CBV for CRUD operations** - Less boilerplate code
2. **Use FBV for custom logic** - More explicit and easier to understand
3. **Keep views thin** - Move business logic to models or separate services
4. **Use get_object_or_404()** - Better than try/except for single object retrieval
5. **Use reverse() for URLs** - Never hardcode URLs
6. **Use mixins for reusable functionality** - DRY principle

---

## Resources

- [Django Views Documentation](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [Class-Based Views](https://docs.djangoproject.com/en/stable/topics/class-based-views/)
- [URL Dispatcher](https://docs.djangoproject.com/en/stable/topics/http/urls/)
- [Request/Response Objects](https://docs.djangoproject.com/en/stable/ref/request-response/)
- [Classy Class-Based Views](https://ccbv.co.uk/) - Visual reference for CBV
