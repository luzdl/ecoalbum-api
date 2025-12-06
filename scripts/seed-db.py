#!/usr/bin/env python
"""
Script para ejecutar el seeding de la base de datos usando seed.sql.
Se ejecuta automáticamente después de las migraciones en Docker.
Usa sqlcmd para ejecutar el SQL de forma confiable.
"""
import os
import sys
import subprocess
import pyodbc


def check_data_exists():
    """Verifica si ya hay datos en la base de datos."""
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '1433')
    db_user = os.environ.get('DB_USER', 'sa')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_name = os.environ.get('DB_NAME', 'master')
    
    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={db_host},{db_port};"
        f"DATABASE={db_name};"
        f"UID={db_user};"
        f"PWD={db_password};"
        f"TrustServerCertificate=yes;"
    )
    
    try:
        conn = pyodbc.connect(connection_string, timeout=10, autocommit=True)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Categoria")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count > 0
    except pyodbc.Error:
        return False


def run_seed():
    """Ejecuta el seeding usando sqlcmd."""
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '1433')
    db_user = os.environ.get('DB_USER', 'sa')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_name = os.environ.get('DB_NAME', 'master')
    
    seed_file = '/app/db/seed.sql'
    
    if not os.path.exists(seed_file):
        print("⚠️ Archivo seed.sql no encontrado. Saltando seeding.")
        return True
    
    # Verificar si ya hay datos
    if check_data_exists():
        print("ℹ️ La base de datos ya tiene datos. Saltando seeding.")
        return True
    
    print("🌱 Ejecutando seeding de la base de datos...")
    
    # Ejecutar sqlcmd
    cmd = [
        '/opt/mssql-tools18/bin/sqlcmd',
        '-S', f'{db_host},{db_port}',
        '-U', db_user,
        '-P', db_password,
        '-d', db_name,
        '-C',
        '-i', seed_file
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        
        if result.returncode == 0:
            print("✅ Seeding completado exitosamente.")
        else:
            print("⚠️ Seeding completado con advertencias.")
        return True
        
    except FileNotFoundError:
        print("⚠️ sqlcmd no disponible.")
        return True
    except Exception as e:
        print(f"⚠️ Error en seeding: {e}")
        return True


if __name__ == "__main__":
    run_seed()
    sys.exit(0)
