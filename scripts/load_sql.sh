#!/bin/bash
# Load SQL Script for ecoalbum-api
# This script loads the database schema and seed data

set -e

echo "=========================================="
echo "EcoAlbum API - Loading Database Scripts"
echo "=========================================="

# Check if sqlcmd is installed
if ! command -v sqlcmd &> /dev/null; then
    echo "Error: sqlcmd not found."
    echo "Please install mssql-tools18 to use this script."
    echo "Linux: apt-get install mssql-tools18"
    echo "macOS: brew install mssql-tools18"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found."
    echo "Run: bash scripts/dev_setup.sh first"
    exit 1
fi

# Source environment variables
export $(cat .env | grep -v '#' | xargs)

# Load schema
if [ -f "db/schema.sql" ]; then
    echo "Loading schema from db/schema.sql..."
    sqlcmd -S "${DB_HOST},${DB_PORT}" -U "${DB_USER}" -P "${DB_PASSWORD}" -d "${DB_NAME}" -i db/schema.sql
    echo "✓ Schema loaded."
else
    echo "Warning: db/schema.sql not found."
fi

# Load seed data
if [ -f "db/seed.sql" ]; then
    echo "Loading seed data from db/seed.sql..."
    sqlcmd -S "${DB_HOST},${DB_PORT}" -U "${DB_USER}" -P "${DB_PASSWORD}" -d "${DB_NAME}" -i db/seed.sql
    echo "✓ Seed data loaded."
else
    echo "Warning: db/seed.sql not found."
fi

echo "=========================================="
echo "✓ Database scripts completed!"
echo "=========================================="
