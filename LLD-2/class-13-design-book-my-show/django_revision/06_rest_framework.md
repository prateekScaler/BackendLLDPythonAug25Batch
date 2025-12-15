# Django REST Framework (DRF)

## What is DRF?

Django REST Framework is a powerful toolkit for building Web APIs in Django. It provides serialization, authentication, permissions, and browsable API features.

---

## Installation & Setup

```bash
pip install djangorestframework
```

### Configure settings.py
```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

---

## Serializers

Serializers convert complex data types (QuerySets, model instances) to Python datatypes that can be rendered into JSON/XML.

### Basic Serializer
```python
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    age = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance
```

### ModelSerializer
```python
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'age', 'created_at']
        # Or all fields
        # fields = '__all__'
        # Or exclude
        # exclude = ['password']

        # Read-only fields
        read_only_fields = ['id', 'created_at']

        # Extra kwargs
        extra_kwargs = {
            'email': {'required': True},
            'age': {'min_value': 0, 'max_value': 150}
        }
```

### Nested Serializers
```python
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'isbn']

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True, source='book_set')
    book_count = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'books', 'book_count']

    def get_book_count(self, obj):
        return obj.book_set.count()
```

### Custom Validation
```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'age']

    def validate_email(self, value):
        """Validate single field"""
        if not value.endswith('@company.com'):
            raise serializers.ValidationError("Must use company email")
        return value

    def validate(self, data):
        """Cross-field validation"""
        if data.get('age') and data['age'] < 18:
            raise serializers.ValidationError("Must be 18 or older")
        return data
```

---

## Views

### APIView (Class-Based)
```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserListView(APIView):
    def get(self, request):
        """List all users"""
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Create a new user"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        """Get single user"""
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        """Update user"""
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete user"""
        user = self.get_object(pk)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

### Function-Based Views
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

---

## Generic Views

### ListCreateAPIView
```python
from rest_framework import generics

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        # Custom filtering
        queryset = super().get_queryset()
        is_active = self.request.query_params.get('is_active')
        if is_active:
            queryset = queryset.filter(is_active=is_active == 'true')
        return queryset
```

### RetrieveUpdateDestroyAPIView
```python
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

### Other Generic Views
```python
# List only
generics.ListAPIView

# Create only
generics.CreateAPIView

# Retrieve only
generics.RetrieveAPIView

# Update only
generics.UpdateAPIView

# Destroy only
generics.DestroyAPIView

# Retrieve + Update
generics.RetrieveUpdateAPIView
```

---

## ViewSets

ViewSets combine logic for multiple related views.

### ModelViewSet
```python
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    """
    Provides `list`, `create`, `retrieve`, `update`, and `destroy` actions
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        # Custom filtering
        queryset = super().get_queryset()
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email__icontains=email)
        return queryset

    def perform_create(self, serializer):
        # Custom logic on create
        serializer.save(created_by=self.request.user)
```

### ReadOnlyModelViewSet
```python
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """Provides only `list` and `retrieve` actions"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
```

### Custom Actions
```python
from rest_framework.decorators import action

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def active(self, request):
        """List active users: GET /users/active/"""
        active_users = User.objects.filter(is_active=True)
        serializer = self.get_serializer(active_users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate user: POST /users/{id}/deactivate/"""
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'status': 'user deactivated'})
```

---

## Routers

Automatically generate URL patterns for ViewSets.

```python
# urls.py
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # other urls
]

urlpatterns += router.urls

# Generated URLs:
# GET    /users/              -> list
# POST   /users/              -> create
# GET    /users/{id}/         -> retrieve
# PUT    /users/{id}/         -> update
# PATCH  /users/{id}/         -> partial_update
# DELETE /users/{id}/         -> destroy
```

### SimpleRouter vs DefaultRouter
```python
from rest_framework.routers import SimpleRouter, DefaultRouter

# SimpleRouter - basic routes only
router = SimpleRouter()

# DefaultRouter - includes API root view
router = DefaultRouter()
```

---

## Authentication

### Session Authentication
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
}
```

### Token Authentication
```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

# Run migrations
# python manage.py migrate
```

**Obtain Token:**
```python
from rest_framework.authtoken.models import Token

# In view or signal
token = Token.objects.create(user=user)
print(token.key)
```

**Use Token:**
```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
     http://localhost:8000/api/users/
```

### JWT Authentication
```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

## Permissions

### Built-in Permissions
```python
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    AllowAny,
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Must be logged in
```

### Custom Permission
```python
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for owner
        return obj.owner == request.user

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]
```

---

## Filtering & Searching

### Install django-filter
```bash
pip install django-filter
```

### Configure
```python
# settings.py
INSTALLED_APPS = [
    # ...
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

### Use in ViewSet
```python
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Filter by exact match
    filterset_fields = ['is_active', 'age']
    # GET /users/?is_active=true&age=25

    # Search
    search_fields = ['name', 'email']
    # GET /users/?search=Aravinda

    # Ordering
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']  # Default ordering
    # GET /users/?ordering=name
    # GET /users/?ordering=-created_at
```

---

## Pagination

### PageNumberPagination
```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# GET /users/?page=2
```

### LimitOffsetPagination
```python
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

# GET /users/?limit=10&offset=20
```

### Custom Pagination
```python
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
```

---

## Throttling

Limit request rates to prevent abuse.

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    }
}
```

---

## Versioning

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
}

# urls.py
urlpatterns = [
    path('api/v1/', include('myapp.urls')),
    path('api/v2/', include('myapp.v2_urls')),
]
```

---

## Error Handling

### Custom Exception Handler
```python
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code

    return response

# settings.py
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'myapp.utils.custom_exception_handler'
}
```

---

## Testing

```python
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

class UserAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(name='jagnesh', email='jagnesh@example.com')

    def test_get_user_list(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        data = {'name': 'Prateek', 'email': 'Prateek@example.com'}
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_authentication(self):
        # Test with token
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
```

---

## Resources

- [DRF Official Documentation](https://www.django-rest-framework.org/)
- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Classy DRF](https://www.cdrf.co/) - Visual reference for DRF classes
- [DRF Cheat Sheet](https://www.django-rest-framework.org/topics/documenting-your-api/)
- [Simple JWT Docs](https://django-rest-framework-simplejwt.readthedocs.io/)
