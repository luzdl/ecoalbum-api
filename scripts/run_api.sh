#!/bin/bash
# Run API Server Script for ecoalbum-api
# This script starts the development server

set -e

echo "=========================================="
echo "EcoAlbum API - Starting Development Server"
echo "=========================================="

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found."
    echo "Run: bash scripts/dev_setup.sh first"
    exit 1
fi

source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found."
    echo "Copy .env.example to .env and fill in your database credentials."
    cp .env.example .env
    echo "Created .env from template. Please edit it with your credentials."
fi

echo "Starting Django development server..."
echo "API will be available at: http://localhost:8000/"
echo "Swagger UI at: http://localhost:8000/api/swagger/"
echo "Health check at: http://localhost:8000/api/health/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver 0.0.0.0:8000
