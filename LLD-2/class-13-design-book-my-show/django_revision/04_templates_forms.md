# Django Templates & Forms

## Templates Overview

Django's template engine allows you to generate HTML dynamically. Templates separate presentation from business logic.

---

## Template Basics

### Template Configuration (settings.py)
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Project-level templates
        'APP_DIRS': True,  # Look for templates in each app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

### Directory Structure
```
myproject/
├── templates/              # Project-level templates
│   └── base.html
└── myapp/
    └── templates/
        └── myapp/          # App-level templates
            ├── list.html
            └── detail.html
```

---

## Template Syntax

### Variables
```django
{{ variable }}
{{ user.name }}
{{ user.email }}
{{ products.0.name }}  <!-- First item in list -->
{{ dict.key }}
```

### Filters
```django
{{ name|lower }}                    <!-- Lowercase -->
{{ name|upper }}                    <!-- Uppercase -->
{{ name|title }}                    <!-- Title Case -->
{{ text|truncatewords:30 }}        <!-- Truncate to 30 words -->
{{ value|default:"Nothing" }}      <!-- Default if empty -->
{{ date|date:"Y-m-d" }}            <!-- Format date -->
{{ price|floatformat:2 }}          <!-- Format decimal -->
{{ html|safe }}                    <!-- Mark as safe HTML -->
{{ text|length }}                  <!-- Length -->
{{ list|join:", " }}               <!-- Join list -->
{{ value|add:5 }}                  <!-- Add 5 -->
```

### Tags

#### if/elif/else
```django
{% if user.is_authenticated %}
    <p>Welcome, {{ user.username }}!</p>
{% elif user.is_anonymous %}
    <p>Please log in.</p>
{% else %}
    <p>Unknown user</p>
{% endif %}
```

#### for loop
```django
{% for product in products %}
    <div>{{ product.name }} - ${{ product.price }}</div>
{% empty %}
    <p>No products available</p>
{% endfor %}

<!-- Loop variables -->
{% for item in items %}
    {{ forloop.counter }}      <!-- 1-indexed counter -->
    {{ forloop.counter0 }}     <!-- 0-indexed counter -->
    {{ forloop.first }}        <!-- True on first iteration -->
    {{ forloop.last }}         <!-- True on last iteration -->
{% endfor %}
```

#### url
```django
<a href="{% url 'user-detail' user_id=user.id %}">View</a>
<a href="{% url 'user-list' %}">All Users</a>
```

#### static
```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/style.css' %}">
<img src="{% static 'images/logo.png' %}">
```

#### include
```django
{% include 'partials/header.html' %}
{% include 'partials/navbar.html' with active='home' %}
```

#### block & extends (Template Inheritance)
```django
<!-- base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}My Site{% endblock %}</title>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>

<!-- list.html -->
{% extends 'base.html' %}

{% block title %}User List{% endblock %}

{% block content %}
    <h1>Users</h1>
    {% for user in users %}
        <p>{{ user.name }}</p>
    {% endfor %}
{% endblock %}
```

#### with
```django
{% with total=products|length %}
    <p>Total products: {{ total }}</p>
{% endwith %}
```

---

## Template Inheritance Example

```django
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}My Site{% endblock %}</title>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav>
        {% block navbar %}
            <a href="{% url 'home' %}">Home</a>
        {% endblock %}
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        {% block footer %}
            <p>&copy; 2024 My Site</p>
        {% endblock %}
    </footer>

    {% block extra_js %}{% endblock %}
</body>
</html>

<!-- templates/users/list.html -->
{% extends 'base.html' %}
{% load static %}

{% block title %}Users - {{ block.super }}{% endblock %}

{% block extra_css %}
    <link rel="stylesheet" href="{% static 'css/users.css' %}">
{% endblock %}

{% block content %}
    <h1>User List</h1>
    <table>
        {% for user in users %}
            <tr>
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
            </tr>
        {% endfor %}
    </table>
{% endblock %}
```

---

## Django Forms

### Creating Forms

#### Form from scratch
```python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    age = forms.IntegerField(required=False)
    subscribe = forms.BooleanField(required=False)

    # Custom validation
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and age < 18:
            raise forms.ValidationError("Must be 18 or older")
        return age

    def clean(self):
        # Cross-field validation
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')

        if name and email and name.lower() in email.lower():
            raise forms.ValidationError("Name cannot be in email")

        return cleaned_data
```

#### ModelForm
```python
from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'age']
        # Or exclude certain fields
        # exclude = ['created_at']

        # Custom labels
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
        }

        # Help text
        help_texts = {
            'email': 'We will never share your email.',
        }

        # Custom widgets
        widgets = {
            'age': forms.NumberInput(attrs={'min': 0, 'max': 150}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
```

---

## Form Field Types

```python
# Text inputs
forms.CharField()
forms.EmailField()
forms.URLField()
forms.SlugField()

# Numeric
forms.IntegerField()
forms.FloatField()
forms.DecimalField()

# Date/Time
forms.DateField()
forms.TimeField()
forms.DateTimeField()

# Boolean
forms.BooleanField()

# Choice
forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
forms.MultipleChoiceField(choices=CHOICES)

# File
forms.FileField()
forms.ImageField()

# Others
forms.RegexField(regex=r'^\d{10}$')  # Phone number
```

---

## Form Widgets

```python
from django import forms

class MyForm(forms.Form):
    # Text inputs
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter name'
    }))

    # Textarea
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 5,
        'cols': 40
    }))

    # Password
    password = forms.CharField(widget=forms.PasswordInput)

    # Hidden input
    user_id = forms.IntegerField(widget=forms.HiddenInput)

    # Select dropdown
    country = forms.ChoiceField(widget=forms.Select, choices=COUNTRIES)

    # Radio buttons
    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('M', 'Male'), ('F', 'Female')]
    )

    # Checkboxes
    interests = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=[('sports', 'Sports'), ('music', 'Music')]
    )

    # Date picker
    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date'
    }))
```

---

## Using Forms in Views

### Function-Based View
```python
from django.shortcuts import render, redirect
from .forms import UserForm

def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()  # For ModelForm
            # Or access cleaned data
            # name = form.cleaned_data['name']
            return redirect('user-detail', user_id=user.id)
    else:
        form = UserForm()

    return render(request, 'users/form.html', {'form': form})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-detail', user_id=user.id)
    else:
        form = UserForm(instance=user)

    return render(request, 'users/form.html', {'form': form})
```

### Class-Based View
```python
from django.views.generic.edit import CreateView, UpdateView
from .models import User
from .forms import UserForm

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('user-list')

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('user-list')
```

---

## Rendering Forms in Templates

### Simple Rendering
```django
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}           <!-- Each field in <p> tags -->
    <!-- OR -->
    {{ form.as_table }}       <!-- Table format -->
    <!-- OR -->
    {{ form.as_ul }}          <!-- Unordered list -->

    <button type="submit">Submit</button>
</form>
```

### Manual Rendering
```django
<form method="post">
    {% csrf_token %}

    <!-- Display non-field errors -->
    {% if form.non_field_errors %}
        <div class="errors">{{ form.non_field_errors }}</div>
    {% endif %}

    <!-- Render each field manually -->
    <div class="field">
        {{ form.name.label_tag }}
        {{ form.name }}
        {% if form.name.errors %}
            <span class="error">{{ form.name.errors }}</span>
        {% endif %}
        {% if form.name.help_text %}
            <small>{{ form.name.help_text }}</small>
        {% endif %}
    </div>

    <div class="field">
        {{ form.email.label_tag }}
        {{ form.email }}
        {{ form.email.errors }}
    </div>

    <button type="submit">Submit</button>
</form>
```

### Loop Through Fields
```django
<form method="post">
    {% csrf_token %}

    {% for field in form %}
        <div class="field">
            {{ field.label_tag }}
            {{ field }}
            {% if field.errors %}
                <div class="errors">{{ field.errors }}</div>
            {% endif %}
            {% if field.help_text %}
                <small>{{ field.help_text }}</small>
            {% endif %}
        </div>
    {% endfor %}

    <button type="submit">Submit</button>
</form>
```

---

## Form Validation

### Field-level Validation
```python
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'age']

    def clean_email(self):
        """Validate email field"""
        email = self.cleaned_data.get('email')

        if not email.endswith('@company.com'):
            raise forms.ValidationError("Must use company email")

        return email

    def clean_age(self):
        """Validate age field"""
        age = self.cleaned_data.get('age')

        if age and age < 18:
            raise forms.ValidationError("Must be 18 or older")

        return age
```

### Form-level Validation
```python
class UserForm(forms.ModelForm):
    confirm_email = forms.EmailField()

    class Meta:
        model = User
        fields = ['name', 'email', 'age']

    def clean(self):
        """Cross-field validation"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirm_email = cleaned_data.get('confirm_email')

        if email and confirm_email and email != confirm_email:
            raise forms.ValidationError("Email addresses must match")

        return cleaned_data
```

---

## File Upload Forms

### Model with FileField
```python
from django.db import models

class Document(models.Model):
    title = forms.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

### Form
```python
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']
```

### View
```python
def upload_file(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('document-list')
    else:
        form = DocumentForm()

    return render(request, 'documents/upload.html', {'form': form})
```

### Template
```django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Upload</button>
</form>
```

---

## Formsets

Work with multiple forms on the same page.

```python
from django.forms import formset_factory
from .forms import UserForm

# Create formset
UserFormSet = formset_factory(UserForm, extra=3)

def manage_users(request):
    if request.method == 'POST':
        formset = UserFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    form.save()
            return redirect('success')
    else:
        formset = UserFormSet()

    return render(request, 'users/formset.html', {'formset': formset})
```

**Template:**
```django
<form method="post">
    {% csrf_token %}
    {{ formset.management_form }}

    {% for form in formset %}
        {{ form.as_p }}
    {% endfor %}

    <button type="submit">Submit</button>
</form>
```

---

## Custom Template Tags & Filters

### Custom Filter
```python
# myapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply value by arg"""
    return value * arg

# Usage in template:
# {% load custom_filters %}
# {{ price|multiply:2 }}
```

### Custom Tag
```python
# myapp/templatetags/custom_tags.py
from django import template

register = template.Library()

@register.simple_tag
def current_time(format_string):
    from datetime import datetime
    return datetime.now().strftime(format_string)

# Usage in template:
# {% load custom_tags %}
# {% current_time "%Y-%m-%d %H:%M" %}
```

---

## Resources

- [Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Template Language Reference](https://docs.djangoproject.com/en/stable/ref/templates/language/)
- [Built-in Template Tags & Filters](https://docs.djangoproject.com/en/stable/ref/templates/builtins/)
- [Django Forms](https://docs.djangoproject.com/en/stable/topics/forms/)
- [Form Fields Reference](https://docs.djangoproject.com/en/stable/ref/forms/fields/)
- [Form Widgets](https://docs.djangoproject.com/en/stable/ref/forms/widgets/)
