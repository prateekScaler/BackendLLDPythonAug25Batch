#!/bin/bash

# Splitwise Django Project Setup Script

echo "╔════════════════════════════════════════════╗"
echo "║   Splitwise Django Project Setup          ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "→ Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "→ Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "→ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "→ Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo ""
echo "→ Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Seed database
echo ""
echo "→ Seeding database with sample data..."
python manage.py seed_data

# Success message
echo ""
echo "╔════════════════════════════════════════════╗"
echo "║   ✓ Setup Complete!                        ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "To start the CLI application, run:"
echo "  python cli.py"
echo ""
echo "To access Django admin, run:"
echo "  python manage.py createsuperuser"
echo "  python manage.py runserver"
echo ""
