#!/usr/bin/env python
"""
Script para convertir seed.sql a formato Unicode compatible con SQL Server.
Lee el archivo original en Latin-1, agrega prefijo N' a los strings y lo guarda en UTF-8.
"""
import os

# Rutas
WINDOWS_DOWNLOADS = r"C:\Users\luces\Downloads\seed.sql"
WINDOWS_DEST = r"C:\Users\luces\OneDrive\Escritorio\yo literal\PROYECTOS VS\ecoalbum-api\db\seed.sql"


def find_string_end(line, start):
    """Encuentra el final de un string SQL, manejando escapes ''."""
    i = start
    while i < len(line):
        if line[i] == "'":
            # Verificar si es escape ''
            if i + 1 < len(line) and line[i + 1] == "'":
                i += 2  # Saltar el escape
            else:
                return i + 1  # Final del string (incluye la comilla)
        else:
            i += 1
    return len(line)


def convert_strings_to_nvarchar(content):
    """
    Convierte strings SQL de 'texto' a N'texto' para soporte Unicode.
    """
    lines = content.split('\n')
    result = []
    
    for line in lines:
        # Si es un comentario o línea vacía, mantener igual
        if line.strip().startswith('--') or not line.strip():
            result.append(line)
            continue
        
        new_line = ""
        i = 0
        while i < len(line):
            # Si encontramos N' ya existente, saltar
            if i < len(line) - 1 and line[i:i+2] == "N'":
                end = find_string_end(line, i + 2)
                new_line += line[i:end]
                i = end
            # Si encontramos ' que inicia un string
            elif line[i] == "'" and (i == 0 or line[i-1] != "'"):
                # Verificar que el caracter anterior no sea N
                if i > 0 and line[i-1] == 'N':
                    new_line += line[i]
                    i += 1
                else:
                    end = find_string_end(line, i + 1)
                    string_content = line[i:end]
                    new_line += "N" + string_content
                    i = end
            else:
                new_line += line[i]
                i += 1
        
        result.append(new_line)
    
    return '\n'.join(result)


def main():
    print("=" * 60)
    print("🔄 Conversión de seed.sql a formato Unicode")
    print("=" * 60)
    
    source = WINDOWS_DOWNLOADS
    dest = WINDOWS_DEST
    
    print(f"📂 Origen: {source}")
    print(f"📂 Destino: {dest}")
    
    if not os.path.exists(source):
        print(f"❌ No se encontró el archivo origen: {source}")
        return 1
    
    # IMPORTANTE: Leer específicamente como Latin-1 (ISO-8859-1)
    # El archivo original está en esta codificación
    print("\n📖 Leyendo archivo original como Latin-1...")
    try:
        with open(source, 'r', encoding='latin-1') as f:
            content = f.read()
        print(f"   ✅ Leído correctamente")
        print(f"   📄 {len(content)} caracteres")
        print(f"   📄 {content.count(chr(10))} líneas")
        
        # Verificar que tiene caracteres especiales correctos
        if 'Mamíferos' in content:
            print("   ✅ Caracteres especiales detectados correctamente (Mamíferos)")
        else:
            print("   ⚠️  No se detectaron caracteres especiales esperados")
            
    except Exception as e:
        print(f"❌ Error leyendo archivo: {e}")
        return 1
    
    # Convertir strings a N'...'
    print("\n🔄 Convirtiendo strings a formato Unicode (N'...')...")
    converted = convert_strings_to_nvarchar(content)
    new_n_quotes = converted.count("N'")
    print(f"   ✅ {new_n_quotes} strings con prefijo N'")
    
    # Guardar archivo en UTF-8 (sin BOM)
    print(f"\n💾 Guardando archivo en UTF-8: {dest}")
    try:
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(converted)
        print("   ✅ Archivo guardado con codificación UTF-8")
    except Exception as e:
        print(f"❌ Error guardando archivo: {e}")
        return 1
    
    # Verificar el archivo guardado
    print("\n🔍 Verificando archivo guardado...")
    with open(dest, 'r', encoding='utf-8') as f:
        saved = f.read()
    if 'Mamíferos' in saved:
        print("   ✅ Caracteres especiales preservados correctamente")
    else:
        print("   ❌ Los caracteres especiales no se guardaron bien")
    
    print("\n" + "=" * 60)
    print("✅ Conversión completada exitosamente!")
    print("=" * 60)
    print("\nSiguientes pasos:")
    print("1. docker-compose down -v")
    print("2. docker-compose up -d --build")
    print("3. Invoke-RestMethod http://localhost:8000/api/fauna/categorias/")
    
    return 0


if __name__ == "__main__":
    exit(main())
