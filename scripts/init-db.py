#!/usr/bin/env python
"""
Script de inicialización de base de datos para EcoAlbum API.
Ejecuta schema.sql para crear tablas, luego fake migrate, luego seed.sql.
"""
import os
import sys
import subprocess
import pyodbc


def get_connection_string():
    """Obtiene el connection string para la base de datos."""
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '1433')
    db_user = os.environ.get('DB_USER', 'sa')
    db_password = os.environ.get('DB_PASSWORD', '')
    db_name = os.environ.get('DB_NAME', 'master')
    
    return (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={db_host},{db_port};"
        f"DATABASE={db_name};"
        f"UID={db_user};"
        f"PWD={db_password};"
        f"TrustServerCertificate=yes;"
        f"Encrypt=no;"
    )


def tables_exist():
    """Verifica si las tablas principales ya existen."""
    try:
        conn = pyodbc.connect(get_connection_string(), timeout=10, autocommit=True)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_NAME IN ('Categoria', 'Animal', 'FotoAnimal', 'Flora', 'Amenaza')
        """)
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return count >= 5  # Todas las tablas principales existen
    except pyodbc.Error:
        return False


def data_exists():
    """Verifica si ya hay datos en las tablas principales."""
    try:
        conn = pyodbc.connect(get_connection_string(), timeout=10, autocommit=True)
        cursor = conn.cursor()
        
        # Verificar que todas las tablas tengan datos
        tables = [
            ('Categoria', 5),
            ('Animal', 50),
            ('FotoAnimal', 50),
            ('Amenaza', 5),
            ('AccionProteccion', 5),
        ]
        
        for table, min_count in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                if count < min_count:
                    cursor.close()
                    conn.close()
                    return False
            except:
                cursor.close()
                conn.close()
                return False
        
        cursor.close()
        conn.close()
        return True
    except pyodbc.Error:
        return False


def run_sql_file(filename, description):
    """Ejecuta un archivo SQL usando pyodbc para soporte correcto de UTF-8."""
    filepath = f'/app/db/{filename}'
    
    if not os.path.exists(filepath):
        print(f"⚠️ Archivo {filename} no encontrado.")
        return False
    
    print(f"📄 Ejecutando {description}...")
    
    try:
        # Leer el archivo SQL en UTF-8
        with open(filepath, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        # Conectar a la base de datos con setencoding para Unicode
        conn = pyodbc.connect(get_connection_string(), timeout=120, autocommit=True)
        # Configurar encoding para Unicode correcto
        conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
        conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
        conn.setencoding(encoding='utf-8')
        cursor = conn.cursor()
        
        import re
        blocks = []
        
        # Verificar si hay separadores GO
        if re.search(r'\nGO\s*\n', sql_content, re.IGNORECASE):
            # Dividir por GO
            blocks = re.split(r'\nGO\s*\n', sql_content, flags=re.IGNORECASE)
        else:
            # Para seed.sql sin GO, dividir por comentarios -- seguidos de INSERT
            current_block = []
            in_statement = False
            
            for line in sql_content.split('\n'):
                stripped = line.strip()
                
                # Comentario que separa bloques (como --Aves, --Inserts, etc.)
                if stripped.startswith('--') and len(stripped) > 2 and not stripped.startswith('-- '):
                    if current_block and in_statement:
                        blocks.append('\n'.join(current_block))
                        current_block = []
                        in_statement = False
                    continue
                
                # Inicio de INSERT
                if stripped.upper().startswith('INSERT INTO'):
                    if current_block and in_statement:
                        blocks.append('\n'.join(current_block))
                        current_block = []
                    in_statement = True
                
                if in_statement:
                    current_block.append(line)
            
            if current_block:
                blocks.append('\n'.join(current_block))
        
        # Ejecutar cada bloque
        executed = 0
        errors = 0
        for i, block in enumerate(blocks):
            block_clean = block.strip()
            if not block_clean:
                continue
            try:
                cursor.execute(block_clean)
                executed += 1
            except pyodbc.Error as e:
                error_msg = str(e)
                # Ignorar errores de "ya existe"
                if 'already' in error_msg.lower() or 'existe' in error_msg.lower():
                    continue
                # Para schema.sql, ignorar ciertos errores
                if filename == 'schema.sql' and ('already' in error_msg.lower() or 'constraint' in error_msg.lower()):
                    continue
                errors += 1
                if errors <= 5:  # Solo mostrar primeros 5 errores
                    print(f"   ⚠️ Error en bloque {i+1}: {error_msg[:200]}")
        
        cursor.close()
        conn.close()
        
        print(f"✅ {description} completado. ({executed} bloques ejecutados)")
        return True
        
    except Exception as e:
        print(f"❌ Error ejecutando {description}: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_django_migrate():
    """Ejecuta las migraciones de Django."""
    print("🔄 Ejecutando migraciones de Django...")
    
    try:
        # Primero makemigrations
        subprocess.run(
            [sys.executable, 'manage.py', 'makemigrations', '--noinput'],
            check=False
        )
        
        # Si las tablas ya existen, usar --fake-initial
        if tables_exist():
            print("ℹ️ Tablas existentes detectadas, usando --fake-initial...")
            result = subprocess.run(
                [sys.executable, 'manage.py', 'migrate', '--fake-initial', '--noinput'],
                capture_output=True,
                text=True
            )
        else:
            result = subprocess.run(
                [sys.executable, 'manage.py', 'migrate', '--noinput'],
                capture_output=True,
                text=True
            )
        
        print("✅ Migraciones completadas.")
        return True
    except Exception as e:
        print(f"⚠️ Error en migraciones: {e}")
        return False


def main():
    """Función principal de inicialización."""
    print("=" * 50)
    print("🚀 Inicializando Base de Datos EcoAlbum")
    print("=" * 50)
    
    # Verificar si ya está todo inicializado
    if data_exists():
        print("ℹ️ Base de datos ya inicializada con datos.")
        print("🔄 Ejecutando migraciones pendientes...")
        run_django_migrate()
        print("✅ Inicialización completada.")
        return
    
    # Paso 1: Ejecutar schema.sql para crear tablas con estructura correcta
    if not tables_exist():
        run_sql_file('schema.sql', 'Schema SQL')
    else:
        print("ℹ️ Tablas ya existen, saltando schema.sql")
    
    # Paso 2: Ejecutar migraciones de Django
    run_django_migrate()
    
    # Paso 3: Ejecutar seed.sql para insertar datos
    if not data_exists():
        run_sql_file('seed.sql', 'Seed SQL')
    else:
        print("ℹ️ Datos ya existen, saltando seed.sql")
    
    print("=" * 50)
    print("✅ Inicialización de base de datos completada.")
    print("=" * 50)


if __name__ == "__main__":
    main()
