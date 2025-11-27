# Run API Server Script for ecoalbum-api (Windows PowerShell)
# This script starts the development server

Write-Host "==========================================" -ForegroundColor Green
Write-Host "EcoAlbum API - Starting Development Server" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green

# Check if venv exists
if (-Not (Test-Path "venv")) {
    Write-Host "Error: Virtual environment not found." -ForegroundColor Red
    Write-Host "Run: .\scripts\dev_setup.ps1 first" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Check if .env exists
if (-Not (Test-Path ".env")) {
    Write-Host "Warning: .env file not found." -ForegroundColor Yellow
    Write-Host "Copy .env.example to .env and fill in your database credentials." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from template. Please edit it with your credentials." -ForegroundColor Cyan
}

Write-Host "Starting Django development server..." -ForegroundColor Yellow
Write-Host "API will be available at: http://localhost:8000/" -ForegroundColor Cyan
Write-Host "Swagger UI at: http://localhost:8000/api/swagger/" -ForegroundColor Cyan
Write-Host "Health check at: http://localhost:8000/api/health/" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow

python manage.py runserver 0.0.0.0:8000
