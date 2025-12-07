#!/usr/bin/env python
"""
Script para corregir caracteres especiales corruptos en la base de datos.
Primero convierte las columnas a NVARCHAR, luego actualiza los datos.
Ejecutar con: docker exec ecoalbum-api python scripts/fix-encoding.py
"""
import os
import pyodbc

def get_connection_string():
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_port = os.environ.get('DB_PORT', '1433')
    db_user = os.environ.get('DB_USER', 'sa')
    db_password = os.environ.get('DB_PASSWORD', 'Preguntadera123!')
    db_name = os.environ.get('DB_NAME', 'SOMETEDERA')
    
    return (
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={db_host},{db_port};"
        f"DATABASE={db_name};"
        f"UID={db_user};"
        f"PWD={db_password};"
        f"TrustServerCertificate=yes;"
    )


def convert_columns_to_nvarchar(cursor):
    """Convierte las columnas VARCHAR/TEXT a NVARCHAR para soportar Unicode."""
    print("  Convirtiendo columnas a NVARCHAR...")
    
    alterations = [
        # Categoria
        "ALTER TABLE Categoria ALTER COLUMN nombre NVARCHAR(50) NOT NULL",
        "ALTER TABLE Categoria ALTER COLUMN descripcion NVARCHAR(500)",
        
        # Amenaza  
        "ALTER TABLE Amenaza ALTER COLUMN nombre NVARCHAR(100) NOT NULL",
        "ALTER TABLE Amenaza ALTER COLUMN descripcion NVARCHAR(MAX)",
        
        # AccionProteccion
        "ALTER TABLE AccionProteccion ALTER COLUMN titulo NVARCHAR(200) NOT NULL",
        "ALTER TABLE AccionProteccion ALTER COLUMN descripcion NVARCHAR(MAX)",
        
        # Animal
        "ALTER TABLE Animal ALTER COLUMN nombre_comun NVARCHAR(200) NOT NULL",
        "ALTER TABLE Animal ALTER COLUMN nombre_cientifico NVARCHAR(200) NOT NULL",
        "ALTER TABLE Animal ALTER COLUMN descripcion NVARCHAR(MAX)",
        "ALTER TABLE Animal ALTER COLUMN habitat NVARCHAR(MAX)",
        "ALTER TABLE Animal ALTER COLUMN distribucion NVARCHAR(MAX)",
        "ALTER TABLE Animal ALTER COLUMN importancia_ecologica NVARCHAR(MAX)",
        "ALTER TABLE Animal ALTER COLUMN estado NVARCHAR(50)",
        
        # Flora
        "ALTER TABLE Flora ALTER COLUMN nombre_comun NVARCHAR(200) NOT NULL",
        "ALTER TABLE Flora ALTER COLUMN nombre_cientifico NVARCHAR(200) NOT NULL",
        "ALTER TABLE Flora ALTER COLUMN descripcion NVARCHAR(MAX)",
        "ALTER TABLE Flora ALTER COLUMN distribucion NVARCHAR(MAX)",
        "ALTER TABLE Flora ALTER COLUMN estado NVARCHAR(50)",
        
        # Fotos
        "ALTER TABLE FotoAnimal ALTER COLUMN descripcion NVARCHAR(500)",
        "ALTER TABLE FotoFlora ALTER COLUMN descripcion NVARCHAR(500)",
    ]
    
    count = 0
    for sql in alterations:
        try:
            cursor.execute(sql)
            count += 1
        except Exception as e:
            # Ignorar errores si ya es NVARCHAR
            pass
    
    print(f"    ✅ {count} columnas convertidas a NVARCHAR")
    return count


# Datos correctos para Categoria
CATEGORIA_DATA = {
    'Aves': 'Las aves son animales vertebrados, de sangre caliente, que se caracterizan principalmente por tener plumas, un pico sin dientes, poner huevos con cáscara dura y son los únicos animales vivos que poseen plumas.',
    'Mamíferos': 'Los mamíferos son vertebrados de sangre caliente, caracterizados por tener glándulas mamarias para alimentar a sus crías, pelo en el cuerpo y ser mayormente vivíparos. Pertenecen a la clase Mammalia.',
    'Reptiles': 'Los reptiles son animales vertebrados, de sangre fría, que se caracterizan por tener piel cubierta de escamas queratinosas y respirar mediante pulmones durante toda su vida. La mayoría ponen huevos con cáscara resistente (ovíparos).',
    'Peces marinos': 'Los peces marinos son vertebrados acuáticos con branquias, escamas y aletas. Son de sangre fría y se reproducen mediante huevos. Habitan exclusivamente en agua salada.',
    'Equinodermos': 'Los equinodermos son animales marinos con simetría radial, como estrellas y erizos de mar. Tienen un esqueleto interno con púas y un sistema vascular acuático único para moverse.',
    'Anfibios': 'Los anfibios son vertebrados que experimentan una metamorfosis, iniciando su vida en el agua con branquias (como renacuajos) y desarrollando pulmones para la vida terrestre adulta. Tienen piel húmeda y permeable.'
}

# Datos correctos para Amenaza
AMENAZA_DATA = [
    (1, 'Tráfico ilegal de vida silvestre', 'Captura, comercio y venta ilegal de animales vivos, pieles, partes del cuerpo o productos derivados.'),
    (2, 'Caza ilegal', 'Cacería no regulada o prohibida que reduce las poblaciones naturales de fauna silvestre.'),
    (3, 'Pérdida de hábitat', 'Destrucción o alteración del ambiente natural donde viven las especies.'),
    (4, 'Degradación del hábitat', 'Deterioro progresivo del ecosistema por actividades humanas, reduciendo la calidad del entorno.'),
    (5, 'Deforestación', 'Tala de bosques para agricultura, ganadería, urbanización o extracción de recursos.'),
    (6, 'Fragmentación del ecosistema', 'División del hábitat en parches aislados, afectando la movilidad y reproducción de las especies.'),
    (7, 'Sobreexplotación comercial', 'Extracción excesiva de individuos para comercio legal o ilegal, disminuyendo las poblaciones.'),
    (8, 'Contaminación', 'Presencia de sustancias químicas, residuos o materiales tóxicos que afectan a la fauna.'),
    (9, 'Cambio climático', 'Alteraciones en temperatura y patrones climáticos que afectan la supervivencia de las especies.'),
]

# Datos correctos para AccionProteccion
ACCION_DATA = [
    (1, 'Evitar el tráfico de vida silvestre', 'No comprar animales silvestres, sus partes, ni apoyar actividades de comercio ilegal.'),
    (2, 'Proteger los bosques y selvas', 'Apoyar iniciativas de conservación, evitar quemas y cuidar áreas naturales cercanas.'),
    (3, 'Reducir la deforestación', 'Promover el uso responsable de la madera y apoyar proyectos de reforestación comunitaria.'),
    (4, 'No cazar animales silvestres', 'Evitar prácticas de caza que afecten poblaciones vulnerables de aves y mamíferos.'),
    (5, 'Conservar las playas de anidación', 'No manejar vehículos sobre playas, evitar luces artificiales y no extraer huevos de tortugas.'),
    (6, 'Proteger ríos y mares', 'Reducir el uso de plásticos, no arrojar basura y apoyar limpiezas de costas y riberas.'),
    (7, 'Evitar la contaminación del agua', 'No desechar aceites, químicos o detergentes en ríos ni drenajes para proteger acuáticos y anfibios.'),
    (8, 'Reportar actividades ilegales', 'Informar a las autoridades sobre caza, tala o tráfico de especies para prevenir daños ecológicos.'),
    (9, 'Usar productos sostenibles', 'Elegir productos certificados, responsables y apoyar comercios que respeten la biodiversidad.'),
    (10, 'Participar en programas de educación ambiental', 'Asistir a talleres, voluntariados y actividades que fomenten la protección de la fauna y flora.'),
]

# Estados de conservación correctos
ESTADOS = {
    'Preocupación menor (LC)': 'Preocupación menor (LC)',
    'Casi amenazado (NT)': 'Casi amenazado (NT)',
    'Vulnerable (VU)': 'Vulnerable (VU)',
    'En peligro (EN)': 'En peligro (EN)',
    'Peligro crítico (CR)': 'Peligro crítico (CR)',
}

def fix_categorias(cursor):
    print("  Corrigiendo Categoria...")
    count = 0
    
    # Eliminar constraint para poder actualizar
    try:
        cursor.execute("ALTER TABLE Categoria DROP CONSTRAINT chk_nombre")
        print("    ℹ️ Constraint chk_nombre eliminado temporalmente")
    except:
        pass
    
    # Primero corregir los nombres de categorías que están corruptos
    cursor.execute("UPDATE Categoria SET nombre = 'Mamíferos' WHERE nombre LIKE 'Mam%feros' OR nombre LIKE 'Mam_feros'")
    if cursor.rowcount > 0:
        count += cursor.rowcount
    
    for nombre, descripcion in CATEGORIA_DATA.items():
        cursor.execute(
            "UPDATE Categoria SET descripcion = ? WHERE nombre = ? OR nombre LIKE ?",
            (descripcion, nombre, nombre.replace('í', '_').replace('á', '_').replace('é', '_').replace('ó', '_').replace('ú', '_'))
        )
        if cursor.rowcount > 0:
            count += cursor.rowcount
    
    # Recrear constraint con valores correctos
    try:
        cursor.execute("""
            ALTER TABLE Categoria ADD CONSTRAINT chk_nombre 
            CHECK (nombre IN ('Aves', 'Mamíferos', 'Reptiles', 'Peces marinos', 'Equinodermos', 'Anfibios'))
        """)
        print("    ℹ️ Constraint chk_nombre recreado con valores correctos")
    except Exception as e:
        print(f"    ⚠️ No se pudo recrear constraint: {e}")
    
    print(f"    ✅ {count} categorías actualizadas")
    return count

def fix_amenazas(cursor):
    print("  Corrigiendo Amenaza...")
    count = 0
    for id_amenaza, nombre, descripcion in AMENAZA_DATA:
        cursor.execute(
            "UPDATE Amenaza SET nombre = ?, descripcion = ? WHERE id_amenaza = ?",
            (nombre, descripcion, id_amenaza)
        )
        if cursor.rowcount > 0:
            count += cursor.rowcount
    print(f"    ✅ {count} amenazas actualizadas")
    return count

def fix_acciones(cursor):
    print("  Corrigiendo AccionProteccion...")
    count = 0
    for id_accion, titulo, descripcion in ACCION_DATA:
        cursor.execute(
            "UPDATE AccionProteccion SET titulo = ?, descripcion = ? WHERE id_accion = ?",
            (titulo, descripcion, id_accion)
        )
        if cursor.rowcount > 0:
            count += cursor.rowcount
    print(f"    ✅ {count} acciones actualizadas")
    return count

def fix_estados_animal(cursor):
    print("  Corrigiendo estados en Animal...")
    
    # Primero eliminar el CHECK constraint
    try:
        cursor.execute("ALTER TABLE Animal DROP CONSTRAINT chk_estado")
        print("    ℹ️ Constraint chk_estado eliminado temporalmente")
    except:
        pass  # Ya no existe
    
    updates = [
        ("UPDATE Animal SET estado = 'Preocupación menor (LC)' WHERE estado LIKE 'Preocupaci%n menor%'"),
        ("UPDATE Animal SET estado = 'Casi amenazado (NT)' WHERE estado LIKE 'Casi amenazado%'"),
        ("UPDATE Animal SET estado = 'Vulnerable (VU)' WHERE estado LIKE 'Vulnerable%'"),
        ("UPDATE Animal SET estado = 'En peligro (EN)' WHERE estado LIKE 'En peligro%'"),
        ("UPDATE Animal SET estado = 'Peligro crítico (CR)' WHERE estado LIKE 'Peligro cr%tico%'"),
    ]
    count = 0
    for sql in updates:
        cursor.execute(sql)
        count += cursor.rowcount
    
    # Recrear el CHECK constraint con valores correctos
    try:
        cursor.execute("""
            ALTER TABLE Animal ADD CONSTRAINT chk_estado 
            CHECK (estado IN ('Preocupación menor (LC)', 'Casi amenazado (NT)', 'Vulnerable (VU)', 'En peligro (EN)', 'Peligro crítico (CR)'))
        """)
        print("    ℹ️ Constraint chk_estado recreado con valores correctos")
    except Exception as e:
        print(f"    ⚠️ No se pudo recrear constraint: {e}")
    
    print(f"    ✅ {count} estados de animal actualizados")
    return count

def fix_estados_flora(cursor):
    print("  Corrigiendo estados en Flora...")
    
    # Primero eliminar el CHECK constraint
    try:
        cursor.execute("ALTER TABLE Flora DROP CONSTRAINT chk_estado_planta")
        print("    ℹ️ Constraint chk_estado_planta eliminado temporalmente")
    except:
        pass  # Ya no existe
    
    updates = [
        ("UPDATE Flora SET estado = 'Preocupación menor (LC)' WHERE estado LIKE 'Preocupaci%n menor%'"),
        ("UPDATE Flora SET estado = 'Vulnerable (VU)' WHERE estado LIKE 'Vulnerable%'"),
        ("UPDATE Flora SET estado = 'En peligro (EN)' WHERE estado LIKE 'En peligro%'"),
        ("UPDATE Flora SET estado = 'Peligro crítico (CR)' WHERE estado LIKE 'Peligro cr%tico%'"),
    ]
    count = 0
    for sql in updates:
        cursor.execute(sql)
        count += cursor.rowcount
    
    # Recrear el CHECK constraint con valores correctos
    try:
        cursor.execute("""
            ALTER TABLE Flora ADD CONSTRAINT chk_estado_planta 
            CHECK (estado IN ('Preocupación menor (LC)', 'Vulnerable (VU)', 'En peligro (EN)', 'Peligro crítico (CR)'))
        """)
        print("    ℹ️ Constraint chk_estado_planta recreado con valores correctos")
    except Exception as e:
        print(f"    ⚠️ No se pudo recrear constraint: {e}")
    
    print(f"    ✅ {count} estados de flora actualizados")
    return count

def fix_animal_texts(cursor):
    """Corrige caracteres especiales en textos de Animal usando patrones de reemplazo."""
    print("  Corrigiendo textos en Animal...")
    
    # Mapeo de patrones corruptos a caracteres correctos
    replacements = [
        # Vocales con tilde
        ('á', 'á'), ('Á', 'Á'),
        ('é', 'é'), ('É', 'É'),
        ('í', 'í'), ('Í', 'Í'),
        ('ó', 'ó'), ('Ó', 'Ó'),
        ('ú', 'ú'), ('Ú', 'Ú'),
        # Eñe
        ('ñ', 'ñ'), ('Ñ', 'Ñ'),
        # Diéresis
        ('ü', 'ü'), ('Ü', 'Ü'),
        # Caracteres de reemplazo comunes
        ('�', ''),  # Eliminar caracteres de reemplazo
    ]
    
    columns = ['nombre_comun', 'descripcion', 'habitat', 'distribucion', 'importancia_ecologica']
    count = 0
    
    for col in columns:
        for corrupt, correct in replacements:
            if corrupt and correct:
                sql = f"UPDATE Animal SET {col} = REPLACE({col}, ?, ?) WHERE {col} LIKE ?"
                cursor.execute(sql, (corrupt, correct, f'%{corrupt}%'))
                count += cursor.rowcount
    
    print(f"    ✅ {count} reemplazos en Animal")
    return count

def fix_flora_texts(cursor):
    """Corrige caracteres especiales en textos de Flora."""
    print("  Corrigiendo textos en Flora...")
    
    replacements = [
        ('á', 'á'), ('Á', 'Á'),
        ('é', 'é'), ('É', 'É'),
        ('í', 'í'), ('Í', 'Í'),
        ('ó', 'ó'), ('Ó', 'Ó'),
        ('ú', 'ú'), ('Ú', 'Ú'),
        ('ñ', 'ñ'), ('Ñ', 'Ñ'),
        ('ü', 'ü'), ('Ü', 'Ü'),
    ]
    
    columns = ['nombre_comun', 'descripcion', 'distribucion']
    count = 0
    
    for col in columns:
        for corrupt, correct in replacements:
            if corrupt and correct:
                sql = f"UPDATE Flora SET {col} = REPLACE({col}, ?, ?) WHERE {col} LIKE ?"
                cursor.execute(sql, (corrupt, correct, f'%{corrupt}%'))
                count += cursor.rowcount
    
    print(f"    ✅ {count} reemplazos en Flora")
    return count

def fix_foto_descriptions(cursor):
    """Corrige descripciones de fotos."""
    print("  Corrigiendo FotoAnimal y FotoFlora...")
    
    replacements = [
        ('á', 'á'), ('é', 'é'), ('í', 'í'), ('ó', 'ó'), ('ú', 'ú'),
        ('ñ', 'ñ'), ('ü', 'ü'),
    ]
    
    count = 0
    for table in ['FotoAnimal', 'FotoFlora']:
        for corrupt, correct in replacements:
            sql = f"UPDATE {table} SET descripcion = REPLACE(descripcion, ?, ?) WHERE descripcion LIKE ?"
            cursor.execute(sql, (corrupt, correct, f'%{corrupt}%'))
            count += cursor.rowcount
    
    print(f"    ✅ {count} reemplazos en fotos")
    return count

def main():
    print("=" * 60)
    print("🔧 Corrección de Caracteres Especiales en Base de Datos")
    print("=" * 60)
    
    try:
        conn = pyodbc.connect(get_connection_string(), autocommit=False)
        cursor = conn.cursor()
        
        # Primero convertir columnas a NVARCHAR
        convert_columns_to_nvarchar(cursor)
        conn.commit()
        
        total = 0
        total += fix_categorias(cursor)
        total += fix_amenazas(cursor)
        total += fix_acciones(cursor)
        total += fix_estados_animal(cursor)
        total += fix_estados_flora(cursor)
        total += fix_animal_texts(cursor)
        total += fix_flora_texts(cursor)
        total += fix_foto_descriptions(cursor)
        
        conn.commit()
        
        print("=" * 60)
        print(f"✅ Corrección completada. {total} actualizaciones realizadas.")
        print("=" * 60)
        
        cursor.close()
        conn.close()
        
    except pyodbc.Error as e:
        print(f"❌ Error de conexión: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
