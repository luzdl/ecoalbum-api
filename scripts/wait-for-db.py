#!/usr/bin/env python
"""
Script para esperar a que SQL Server esté listo antes de iniciar Django.
Útil en Docker Compose para manejar el orden de inicio de servicios.
"""
import os
import sys
import time
import pyodbc


def wait_for_db(max_retries=30, retry_interval=2):
    """
    Espera a que la base de datos SQL Server esté disponible.
    
    Args:
        max_retries: Número máximo de intentos
        retry_interval: Segundos entre intentos
    """
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '1433')
    db_user = os.environ.get('DB_USER', 'sa')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_name = os.environ.get('DB_NAME', 'master')
    
    connection_string = (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={db_host},{db_port};"
        f"DATABASE=master;"
        f"UID={db_user};"
        f"PWD={db_password};"
        f"TrustServerCertificate=yes;"
    )
    
    print(f"🔄 Esperando a SQL Server en {db_host}:{db_port}...")
    
    for attempt in range(1, max_retries + 1):
        try:
            # autocommit=True es necesario para CREATE DATABASE
            conn = pyodbc.connect(connection_string, timeout=5, autocommit=True)
            cursor = conn.cursor()
            
            # Verificar si la base de datos existe
            cursor.execute(f"SELECT name FROM sys.databases WHERE name = ?", (db_name,))
            db_exists = cursor.fetchone()
            
            if not db_exists:
                print(f"📦 Creando base de datos '{db_name}'...")
                cursor.execute(f"CREATE DATABASE [{db_name}]")
                print(f"✅ Base de datos '{db_name}' creada exitosamente.")
            
            cursor.close()
            conn.close()
            
            print(f"✅ SQL Server está listo! Base de datos '{db_name}' disponible.")
            return True
            
        except pyodbc.Error as e:
            print(f"⏳ Intento {attempt}/{max_retries}: SQL Server no está listo aún...")
            if attempt < max_retries:
                time.sleep(retry_interval)
            else:
                print(f"❌ Error: No se pudo conectar a SQL Server después de {max_retries} intentos.")
                print(f"   Detalle: {e}")
                return False
    
    return False


if __name__ == "__main__":
    if not wait_for_db():
        sys.exit(1)
    sys.exit(0)
