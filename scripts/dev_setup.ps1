# Development Setup Script for ecoalbum-api (Windows PowerShell)
# This script sets up the development environment on Windows

Write-Host "==========================================" -ForegroundColor Green
Write-Host "EcoAlbum API - Development Setup (Windows)" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check Python version
Write-Host "`nChecking Python version..." -ForegroundColor Yellow
python --version

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (-Not (Test-Path "venv")) {
    python -m venv venv
    Write-Host "Virtual environment created." -ForegroundColor Green
} else {
    Write-Host "Virtual environment already exists." -ForegroundColor Cyan
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if .env exists
if (-Not (Test-Path ".env")) {
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ".env created. Please edit it with your database credentials." -ForegroundColor Cyan
}

# Generate Django secret key if not exists
if (-Not (Select-String -Path ".env" -Pattern "SECRET_KEY=" -Quiet)) {
    Write-Host "Generating Django SECRET_KEY..." -ForegroundColor Yellow
    $SECRET_KEY = python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    Add-Content -Path ".env" -Value "SECRET_KEY=$SECRET_KEY"
    Write-Host "SECRET_KEY generated and added to .env" -ForegroundColor Green
}

# Run migrations
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py migrate

Write-Host "==========================================" -ForegroundColor Green
Write-Host "✓ Development environment ready!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "1. Edit .env file with your database credentials" -ForegroundColor Cyan
Write-Host "2. Run: .\scripts\run_api.ps1" -ForegroundColor Cyan
Write-Host "3. Visit: http://localhost:8000/api/swagger/" -ForegroundColor Cyan
