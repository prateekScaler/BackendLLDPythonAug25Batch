# Django Security & Deployment

## Security Best Practices

### 1. Settings Configuration

#### SECRET_KEY
```python
# NEVER commit SECRET_KEY to version control
# Use environment variables

# settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')

# .env
SECRET_KEY=your-secret-key-here
```

**Generate new SECRET_KEY:**
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### DEBUG Mode
```python
# NEVER set DEBUG=True in production
DEBUG = config('DEBUG', default=False, cast=bool)

# In production
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

---

### 2. Authentication & Authorization

#### Password Hashing
```python
# Django uses PBKDF2 by default
# PASSWORD_HASHERS in settings.py (default is secure)

from django.contrib.auth.hashers import make_password, check_password

# Hash password
hashed = make_password('mypassword')

# Verify password
is_valid = check_password('mypassword', hashed)
```

#### Password Validation
```python
# settings.py
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8}
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

#### User Permissions
```python
from django.contrib.auth.decorators import permission_required, login_required

@login_required
def my_view(request):
    # Only authenticated users
    pass

@permission_required('app.add_model')
def admin_view(request):
    # Only users with specific permission
    pass
```

---

### 3. CSRF Protection

Django includes CSRF protection by default.

```python
# In forms (templates)
<form method="post">
    {% csrf_token %}
    <!-- form fields -->
</form>

# In AJAX requests
// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Include in AJAX headers
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(data)
});
```

---

### 4. SQL Injection Prevention

**Always use Django ORM** - it prevents SQL injection by default.

```python
# SAFE - Django ORM escapes values
User.objects.filter(email=user_input)

# DANGEROUS - Raw SQL
User.objects.raw(f"SELECT * FROM users WHERE email = '{user_input}'")

# If you must use raw SQL, use parameters
User.objects.raw("SELECT * FROM users WHERE email = %s", [user_input])
```

---

### 5. XSS (Cross-Site Scripting) Prevention

**Django templates auto-escape by default.**

```django
<!-- Safe - auto-escaped -->
<p>{{ user_input }}</p>

<!-- Dangerous - marks as safe HTML -->
<p>{{ user_input|safe }}</p>

<!-- Only use |safe with trusted content -->
<p>{{ admin_content|safe }}</p>
```

---

### 6. Sensitive Data Protection

#### Encrypted Fields
```bash
pip install django-encrypted-model-fields
```

```python
from encrypted_model_fields.fields import EncryptedCharField

class Payment(models.Model):
    card_number = EncryptedCharField(max_length=16)
    cvv = EncryptedCharField(max_length=4)

# settings.py
FIELD_ENCRYPTION_KEY = config('FIELD_ENCRYPTION_KEY')
```

#### Environment Variables
```python
# Install python-decouple
pip install python-decouple

# .env file
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# settings.py
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
```

---

### 7. HTTPS & Security Headers

```python
# settings.py

# HTTPS Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS (HTTP Strict Transport Security)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Content Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
```

---

### 8. Rate Limiting

```bash
pip install django-ratelimit
```

```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    # Allow only 5 login attempts per minute per IP
    pass
```

---

### 9. Input Validation

```python
from django import forms

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'age']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@company.com'):
            raise forms.ValidationError("Must use company email")
        return email

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 0 or age > 150:
            raise forms.ValidationError("Invalid age")
        return age
```

---

## Production Deployment

### 1. Checklist Before Deployment

```bash
# Run Django's deployment checklist
python manage.py check --deploy
```

**Critical settings:**
```python
# settings.py (production)

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database - Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Static & Media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

### 2. Static Files

```bash
# Collect static files
python manage.py collectstatic

# Install whitenoise for serving static files
pip install whitenoise
```

```python
# settings.py
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    # ...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

### 3. Database Migrations

```bash
# Production migration workflow
python manage.py makemigrations --check  # Check for missing migrations
python manage.py migrate --plan          # Preview migrations
python manage.py migrate                 # Apply migrations
```

---

### 4. WSGI Servers

#### Gunicorn
```bash
pip install gunicorn

# Run server
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000

# With workers
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

#### uWSGI
```bash
pip install uwsgi

# Run server
uwsgi --http :8000 --module myproject.wsgi
```

---

### 5. Nginx Configuration

```nginx
# /etc/nginx/sites-available/myproject

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /path/to/myproject/staticfiles/;
    }

    location /media/ {
        alias /path/to/myproject/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

### 6. Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Run gunicorn
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### docker-compose.yml
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

---

### 7. AWS Deployment

#### EC2 Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx postgresql -y

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Setup PostgreSQL
sudo -u postgres psql
CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
\q

# Run migrations
python manage.py migrate
python manage.py collectstatic

# Setup Gunicorn systemd service
sudo nano /etc/systemd/system/gunicorn.service
```

**gunicorn.service:**
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/myproject
ExecStart=/home/ubuntu/myproject/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/ubuntu/myproject/myproject.sock \
          myproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Start services
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl restart nginx
```

#### S3 for Static/Media Files
```bash
pip install django-storages boto3
```

```python
# settings.py
INSTALLED_APPS += ['storages']

# AWS Settings
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = 'us-east-1'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# Static files
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

# Media files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

---

### 8. Monitoring & Logging

#### Sentry for Error Tracking
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn=config('SENTRY_DSN'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True
)
```

#### Django Logging
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/django.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

### 9. Performance Optimization

#### Database Optimization
```python
# Use select_related and prefetch_related
User.objects.select_related('profile').all()

# Database indexing
class User(models.Model):
    email = models.EmailField(db_index=True)

# Database connection pooling
pip install django-db-connection-pool
```

#### Caching
```python
# settings.py

# Redis cache
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Cache middleware
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    # ... other middleware
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# Per-view caching
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def my_view(request):
    pass
```

---

### 10. Backup Strategy

```bash
# Database backup
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json

# PostgreSQL backup
pg_dump mydb > backup.sql

# Restore PostgreSQL
psql mydb < backup.sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump mydb > /backups/db_backup_$DATE.sql
```

---

## Security Checklist

- [ ] DEBUG = False in production
- [ ] SECRET_KEY in environment variable
- [ ] ALLOWED_HOSTS configured
- [ ] HTTPS enabled (SSL certificate)
- [ ] Security headers configured
- [ ] CSRF protection enabled
- [ ] SQL injection prevention (use ORM)
- [ ] XSS prevention (template auto-escaping)
- [ ] Strong password policies
- [ ] Rate limiting on sensitive endpoints
- [ ] Sensitive data encrypted
- [ ] Environment variables for secrets
- [ ] Regular security updates
- [ ] Database backups automated
- [ ] Error logging configured
- [ ] Static files served efficiently

---

## Resources

### Security
- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Mozilla Observatory](https://observatory.mozilla.org/)
- [Security Headers](https://securityheaders.com/)

### Deployment
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Digital Ocean Django Tutorials](https://www.digitalocean.com/community/tutorials?q=django)
- [AWS Django Deployment](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)
- [Heroku Django Deployment](https://devcenter.heroku.com/articles/django-app-configuration)

### Monitoring
- [Sentry for Django](https://docs.sentry.io/platforms/python/guides/django/)
- [New Relic](https://docs.newrelic.com/docs/agents/python-agent/)
- [Datadog](https://docs.datadoghq.com/integrations/django/)
