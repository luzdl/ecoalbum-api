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


def get_connection():
    """Obtiene conexión a la base de datos."""
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
    return pyodbc.connect(connection_string, timeout=10, autocommit=True)


def check_all_data_exists():
    """Verifica si TODAS las tablas tienen datos."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        tables_to_check = [
            ('Categoria', 6),
            ('Animal', 60),
            ('FotoAnimal', 60),
            ('Amenaza', 5),
            ('AccionProteccion', 5),
            ('Flora', 10),
        ]
        
        for table, min_count in tables_to_check:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                if count < min_count:
                    cursor.close()
                    conn.close()
                    return False
            except pyodbc.Error:
                cursor.close()
                conn.close()
                return False
        
        cursor.close()
        conn.close()
        return True
    except pyodbc.Error:
        return False


def clear_tables():
    """Vacía todas las tablas en orden correcto (respetando FK)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Orden inverso para respetar foreign keys
        tables_to_clear = [
            'AnimalAccionProteccion',
            'AnimalAmenaza',
            'FotoFlora',
            'FotoAnimal',
            'Flora',
            'AccionProteccion',
            'Amenaza',
            'Animal',
            'Categoria',
        ]
        
        for table in tables_to_clear:
            try:
                cursor.execute(f"DELETE FROM {table}")
                # Reset identity
                cursor.execute(f"DBCC CHECKIDENT ('{table}', RESEED, 0)")
            except pyodbc.Error as e:
                # Tabla puede no existir aún
                pass
        
        cursor.close()
        conn.close()
        print("🗑️ Tablas vaciadas para re-seeding.")
        return True
    except pyodbc.Error as e:
        print(f"⚠️ Error limpiando tablas: {e}")
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
    
    # Verificar si TODAS las tablas tienen datos suficientes
    if check_all_data_exists():
        print("ℹ️ La base de datos ya tiene todos los datos. Saltando seeding.")
        return True
    
    # Limpiar tablas antes de insertar para evitar duplicados
    print("🧹 Limpiando tablas para seeding limpio...")
    clear_tables()
    
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
            if result.stderr:
                print(f"   Detalles: {result.stderr[:200]}")
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
