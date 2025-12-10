# Django Admin Interface

## Admin Overview

Django's admin interface is an auto-generated interface for managing your application's data. It's highly customizable and production-ready.

---

## Basic Setup

### Enable Admin
```python
# settings.py
INSTALLED_APPS = [
    'django.contrib.admin',  # Already included by default
    'django.contrib.auth',
    'django.contrib.contenttypes',
    # ...
]

# urls.py
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
```

### Create Superuser
```bash
python manage.py createsuperuser
# Enter username, email, and password
```

### Register Models
```python
# myapp/admin.py
from django.contrib import admin
from .models import User

# Simple registration
admin.site.register(User)
```

---

## ModelAdmin Customization

### Basic ModelAdmin
```python
from django.contrib import admin
from .models import User

@admin.register(User)  # Decorator registration
class UserAdmin(admin.ModelAdmin):
    # Fields to display in list view
    list_display = ('name', 'email', 'age', 'is_active', 'created_at')

    # Fields to filter by (right sidebar)
    list_filter = ('is_active', 'created_at')

    # Fields to search
    search_fields = ('name', 'email')

    # Fields to order by
    ordering = ('-created_at',)

    # Number of items per page
    list_per_page = 25

# Alternative registration
# admin.site.register(User, UserAdmin)
```

### List Display Customization
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age_group', 'account_status', 'member_since')

    def age_group(self, obj):
        """Custom column showing age group"""
        if obj.age < 18:
            return 'Minor'
        elif obj.age < 65:
            return 'Adult'
        return 'Senior'
    age_group.short_description = 'Age Group'

    def account_status(self, obj):
        """Custom column with colored status"""
        if obj.is_active:
            return format_html('<span style="color: green;">Active</span>')
        return format_html('<span style="color: red;">Inactive</span>')
    account_status.short_description = 'Status'

    def member_since(self, obj):
        """Format created_at"""
        return obj.created_at.strftime('%Y-%m-%d')
    member_since.short_description = 'Member Since'
```

### List Links
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active')

    # Make these fields clickable links to detail page
    list_display_links = ('name', 'email')

    # Make these fields editable directly in list view
    list_editable = ('is_active',)
```

---

## Search & Filtering

### Search Configuration
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Search in these fields
    search_fields = ('name', 'email', 'phone')

    # Use 'icontains' by default, can customize:
    # search_fields = ('=email',)  # Exact match
    # search_fields = ('^name',)   # Starts with
    # search_fields = ('@bio',)    # Full-text search (PostgreSQL)
```

### List Filters
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = (
        'is_active',
        'created_at',
        ('age', admin.EmptyFieldListFilter),  # Has age / No age
    )
```

### Custom Filter
```python
class AgeRangeFilter(admin.SimpleListFilter):
    title = 'age range'
    parameter_name = 'age_range'

    def lookups(self, request, model_admin):
        return (
            ('child', 'Children (< 18)'),
            ('adult', 'Adults (18-65)'),
            ('senior', 'Seniors (> 65)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'child':
            return queryset.filter(age__lt=18)
        if self.value() == 'adult':
            return queryset.filter(age__gte=18, age__lte=65)
        if self.value() == 'senior':
            return queryset.filter(age__gt=65)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = (AgeRangeFilter,)
```

---

## Form Customization

### Field Organization
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Fields to show in form
    fields = ('name', 'email', 'age', 'is_active')

    # Or exclude certain fields
    # exclude = ('created_at', 'updated_at')

    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'id')

    # Group fields into fieldsets
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'age')
        }),
        ('Account Settings', {
            'fields': ('is_active', 'password'),
            'classes': ('collapse',)  # Collapsible section
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
```

### Autocomplete Fields
```python
# For ForeignKey with many related objects
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    autocomplete_fields = ['author']  # Author must have search_fields defined

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']  # Required for autocomplete
```

### Raw ID Fields
```python
# Alternative to dropdown for ForeignKey
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    raw_id_fields = ('author',)
```

---

## Inline Models

Edit related models on the same page.

### TabularInline
```python
from django.contrib import admin
from .models import Author, Book

class BookInline(admin.TabularInline):
    model = Book
    extra = 1  # Number of empty forms
    fields = ('title', 'isbn', 'published_date')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ('name', 'email', 'book_count')

    def book_count(self, obj):
        return obj.book_set.count()
    book_count.short_description = 'Books'
```

### StackedInline
```python
class BookInline(admin.StackedInline):
    model = Book
    extra = 1
    # Fields shown vertically (better for many fields)
```

---

## Actions

Perform bulk operations on selected items.

### Custom Action
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'is_active')
    actions = ['make_active', 'make_inactive', 'delete_selected']

    @admin.action(description='Mark selected users as active')
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} users marked as active.')

    @admin.action(description='Mark selected users as inactive')
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)

    # Remove default delete action
    # def get_actions(self, request):
    #     actions = super().get_actions(request)
    #     if 'delete_selected' in actions:
    #         del actions['delete_selected']
    #     return actions
```

---

## Permissions

### Override Permissions
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only superuser can add
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        # No one can delete
        return False

    def has_change_permission(self, request, obj=None):
        # Everyone with access can edit
        return True

    def get_queryset(self, request):
        # Show only active users to non-superusers
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_active=True)
```

---

## Custom Methods

### Save/Delete Override
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Custom logic before saving
        if not change:  # Creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Custom logic before deleting
        # Log the deletion
        print(f"User {obj.name} deleted by {request.user}")
        super().delete_model(request, obj)
```

---

## Advanced Customization

### Custom Form
```python
from django import forms
from django.contrib import admin
from .models import User

class UserAdminForm(forms.ModelForm):
    # Add custom field
    send_email = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = User
        fields = '__all__'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@company.com'):
            raise forms.ValidationError("Must use company email")
        return email

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
```

### Custom Templates
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Override templates
    change_list_template = 'admin/custom_change_list.html'
    change_form_template = 'admin/custom_change_form.html'
```

### Custom URLs & Views
```python
from django.urls import path
from django.shortcuts import render

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export/', self.export_users, name='export_users'),
        ]
        return custom_urls + urls

    def export_users(self, request):
        # Custom view
        users = User.objects.all()
        # Generate CSV or Excel
        return render(request, 'admin/export.html', {'users': users})
```

---

## Admin Site Customization

```python
# myapp/admin.py
from django.contrib import admin

# Customize admin site
admin.site.site_header = "My Admin Panel"
admin.site.site_title = "My Admin"
admin.site.index_title = "Welcome to My Admin Panel"
```

---

## Many-to-Many Fields

### Horizontal Filter
```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'permissions')  # Side-by-side selection
    # Or vertical
    # filter_vertical = ('groups',)
```

---

## Date Hierarchy

```python
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'  # Date drill-down navigation
```

---

## Prepopulated Fields

```python
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate slug from title
```

---

## Best Practices

1. **Use list_display** for quick overview of data
2. **Add search_fields** for large datasets
3. **Use list_filter** for common filtering needs
4. **Add readonly_fields** for audit fields (created_at, updated_at)
5. **Use inlines** for related models to reduce clicks
6. **Add custom actions** for bulk operations
7. **Override permissions** for fine-grained access control
8. **Add custom methods** for calculated fields
9. **Use fieldsets** to organize complex forms

---

## Resources

- [Django Admin Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)
- [ModelAdmin Options](https://docs.djangoproject.com/en/stable/ref/contrib/admin/#modeladmin-options)
- [Admin Actions](https://docs.djangoproject.com/en/stable/ref/contrib/admin/actions/)
- [Django Admin Cookbook](https://books.agiliq.com/projects/django-admin-cookbook/en/latest/)
