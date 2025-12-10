# Django & Git Comprehensive Revision Guide

A complete, sequential guide for mastering Django framework and Git version control.

---

## 📚 Table of Contents

### Django Framework

1. **[Django Basics & Setup](01_django_basics_setup.md)**
   - Installation & project structure
   - MVT pattern
   - Settings configuration
   - Essential commands
   - Environment variables

2. **[Models & Database](02_models_database.md)**
   - Model field types
   - Relationships (ForeignKey, ManyToMany, OneToOne)
   - QuerySet API
   - Database optimization (select_related, prefetch_related)
   - Migrations

3. **[Views & URLs](03_views_urls.md)**
   - Function-Based Views (FBV)
   - Class-Based Views (CBV)
   - Generic views
   - ViewSets
   - URL routing & patterns
   - Request/Response objects

4. **[Templates & Forms](04_templates_forms.md)**
   - Template syntax & filters
   - Template inheritance
   - Django Forms
   - ModelForms
   - Form validation
   - File uploads

5. **[Admin Interface](05_admin.md)**
   - Admin setup
   - ModelAdmin customization
   - List display & filtering
   - Inline models
   - Custom actions
   - Permissions

6. **[Django REST Framework](06_rest_framework.md)**
   - Serializers
   - API Views (APIView, ViewSets)
   - Authentication (Token, JWT)
   - Permissions
   - Filtering & pagination
   - Testing APIs

### Git Version Control

7. **[Git Essentials](07_git_essentials.md)**
   - Git workflow & basics
   - Branching & merging
   - Remote repositories
   - Advanced commands (rebase, cherry-pick, bisect)
   - Best practices
   - **Practice resources & interactive tutorials**

### Security & Deployment

8. **[Security & Deployment](08_security_deployment.md)**
   - Security best practices
   - HTTPS & security headers
   - Password hashing
   - Production deployment checklist
   - Docker deployment
   - AWS deployment
   - Monitoring & logging

---

## 🎯 How to Use This Guide

### For Complete Beginners
Start from **01_django_basics_setup.md** and progress sequentially through all files.

### For Quick Revision
Jump to specific topics using the table of contents above.

### For Interview Preparation
Focus on:
- Models & QuerySet API (File 02)
- Views & URLs (File 03)
- REST Framework (File 06)
- Git essentials (File 07)
- Security best practices (File 08)

### For Project Work
Reference:
- Admin customization (File 05)
- Forms & validation (File 04)
- Deployment (File 08)

---

## 🔥 Key Features

- ✅ **Sequential Learning Path** - Structured from basics to advanced
- ✅ **Practical Code Examples** - Real-world, copy-paste ready code
- ✅ **Best Practices** - Industry-standard approaches
- ✅ **Comprehensive Coverage** - From setup to production deployment
- ✅ **Git Mastery** - Complete Git guide with practice resources
- ✅ **Security Focus** - Production-ready security practices
- ✅ **Quick Reference** - Easy to find specific topics

---

## 📖 External Resources

### Official Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Git Documentation](https://git-scm.com/doc)

### Interactive Learning
- [Django Girls Tutorial](https://tutorial.djangogirls.org/)
- [Learn Git Branching](https://learngitbranching.js.org/)
- [Git Immersion](https://gitimmersion.com/)

### Books
- [Django for Beginners](https://djangoforbeginners.com/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x)
- [Pro Git Book](https://git-scm.com/book/en/v2)

### Video Courses
- [Corey Schafer - Django Tutorial](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
- [Traversy Media - Django Crash Course](https://www.youtube.com/watch?v=e1IyzVyrLSU)

---

## 🛠️ Quick Start Commands

### Django
```bash
# Install Django
pip install django djangorestframework

# Create project
django-admin startproject myproject
cd myproject

# Create app
python manage.py startapp myapp

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

### Git
```bash
# Initialize repository
git init

# Clone repository
git clone https://github.com/user/repo.git

# Basic workflow
git status
git add .
git commit -m "Your message"
git push origin main

# Create branch
git checkout -b feature-name
```

---

## 💡 Pro Tips

1. **Practice by Building** - Create small projects to apply concepts
2. **Read Documentation** - Django docs are excellent
3. **Use Virtual Environments** - Always isolate project dependencies
4. **Commit Often** - Small, meaningful commits are better
5. **Learn PostgreSQL** - More powerful than SQLite for production
6. **Master Django ORM** - Avoid raw SQL queries
7. **Test Your Code** - Write tests as you develop
8. **Security First** - Never commit secrets, always validate input

---

## 📝 Suggested Learning Path

### Week 1-2: Django Fundamentals
- Files 01-04 (Basics, Models, Views, Templates)
- Build: Simple blog or todo app

### Week 3: Django Advanced
- Files 05-06 (Admin, REST Framework)
- Build: RESTful API for your app

### Week 4: Git & Deployment
- File 07 (Git)
- File 08 (Security & Deployment)
- Deploy your app to cloud platform

---

## 🤝 Contributing

Found an error or want to add something? Feel free to suggest improvements!

---

## 📜 License

This guide is created for educational purposes.

---

**Happy Learning! 🚀**
