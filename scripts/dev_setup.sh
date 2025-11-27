#!/bin/bash
# Development Setup Script for ecoalbum-api
# This script sets up the development environment

set -e

echo "=========================================="
echo "EcoAlbum API - Development Setup"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python --version

# Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Generate Django secret key if not exists
if ! grep -q "SECRET_KEY=" .env; then
    echo "Generating Django SECRET_KEY..."
    SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
    echo "SECRET_KEY=$SECRET_KEY" >> .env
    echo "SECRET_KEY generated and added to .env"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

echo "=========================================="
echo "✓ Development environment ready!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database credentials"
echo "2. Run: bash scripts/run_api.sh"
echo "3. Visit: http://localhost:8000/api/swagger/"
