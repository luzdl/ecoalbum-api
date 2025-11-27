# INICIO RÁPIDO - EcoAlbum API (Windows)

## ¡Bienvenido! 👋

Esta guía te ayudará a iniciar EcoAlbum API en Windows en menos de 10 minutos.

---

## 1️⃣ Requisitos Previos

Antes de comenzar, verifica que tienes:

### Python 3.12+
```powershell
python --version
```
Si no lo tienes, descarga desde: https://www.python.org/downloads/

### ODBC Driver 18 para SQL Server
```powershell
# Verificar si está instalado
odbcconf /A {REGSVR "c:\Program Files\Microsoft ODBC Driver 18 for SQL Server\msodbcsql18.dll"}
```
Si no lo tienes, descarga desde:
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### SQL Server Accesible
Asegúrate de que SQL Server está corriendo en tu máquina o red.

---

## 2️⃣ Configuración Inicial (Primera Vez)

### Paso 1: Abre PowerShell en el directorio del proyecto
```powershell
cd "C:\Users\luces\OneDrive\Escritorio\yo literal\PROYECTOS VS\ecoalbum-api"
```

### Paso 2: Ejecuta el script de setup
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\scripts\dev_setup.ps1
```

Este script:
- ✅ Crea el entorno virtual (venv)
- ✅ Instala todas las dependencias
- ✅ Genera SECRET_KEY automáticamente
- ✅ Configura la base de datos

### Paso 3: Edita el archivo `.env`
```powershell
# Abre el archivo con tu editor favorito
notepad .env
# o
code .env  # Si tienes VS Code
```

Completa estas variables con tus datos de SQL Server:
```env
DB_ENGINE=mssql
DB_NAME=ecoalbum_db          # ← Nombre de tu base de datos
DB_HOST=localhost            # ← Tu servidor SQL Server
DB_PORT=1433                 # ← Puerto (usualmente 1433)
DB_USER=sa                   # ← Tu usuario SQL Server
DB_PASSWORD=YourPassword123! # ← Tu contraseña
```

---

## 3️⃣ Ejecutar el Servidor

### Opción A: Usar script (Recomendado)
```powershell
.\scripts\run_api.ps1
```

### Opción B: Manualmente
```powershell
# Activar venv
.\venv\Scripts\Activate.ps1

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

Verás algo como:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## 4️⃣ Verificar que Funciona ✅

Abre una nueva terminal PowerShell y ejecuta:

```powershell
# Health check (API activa)
curl http://localhost:8000/api/health/

# Resultado esperado:
# {
#   "status": "healthy",
#   "database": "connected",
#   ...
# }
```

---

## 5️⃣ Acceder a la API

### 🌐 Swagger UI (Interfaz Interactiva)
```
http://localhost:8000/api/swagger/
```
Aquí puedes probar todos los endpoints directamente desde el navegador.

### 📚 ReDoc (Documentación Elegante)
```
http://localhost:8000/api/schema/
```

### 🔌 Endpoints Principales

**Listar todas las categorías:**
```powershell
curl http://localhost:8000/api/categories/
```

**Buscar especies:**
```powershell
curl "http://localhost:8000/api/species/?q=harpy"
```

**Filtrar por riesgo:**
```powershell
curl "http://localhost:8000/api/species/?risk_level=VU"
```

**Filtrar endémicas:**
```powershell
curl "http://localhost:8000/api/species/?endemic=true"
```

---

## 🔄 Uso Diario

Una vez completada la instalación:

### Iniciar servidor
```powershell
.\scripts\run_api.ps1
```

### Hacer cambios en modelos
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Ejecutar tests
```powershell
python manage.py test
```

### Acceder a Django Admin
```
http://localhost:8000/admin/
# Usuario: admin (si lo creaste)
```

---

## 🚨 Troubleshooting

### Error: "python: command not found"
**Solución**: Python no está en PATH. 
- Reinstala Python marcando la opción "Add Python to PATH"

### Error: "ODBC Driver not found"
**Solución**: Instala ODBC Driver 18 desde:
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

### Error: "Connection to database failed"
**Solución**: Verifica que:
1. SQL Server está corriendo
2. Las credenciales en .env son correctas
3. El host/puerto son accesibles

### Error: "Port 8000 in use"
**Solución**: Especifica otro puerto
```powershell
python manage.py runserver 0.0.0.0:8001
```

### Error: "cannot import name 'HealthCheckView'"
**Solución**: Ejecuta migraciones
```powershell
python manage.py migrate
```

---

## 📋 Checklist Rápido

```
☐ Python 3.12+ instalado
☐ ODBC Driver 18 instalado
☐ SQL Server accesible
☐ .\scripts\dev_setup.ps1 ejecutado
☐ .env completado con credenciales
☐ .\scripts\run_api.ps1 ejecutado
☐ curl http://localhost:8000/api/health/ retorna "healthy"
☐ http://localhost:8000/api/swagger/ accesible
```

---

## 📖 Documentación Completa

Para más información, consulta:
- **README.md** - Guía exhaustiva
- **ENTORNO_NECESARIO.md** - Requisitos detallados
- **GENERATION_SUMMARY.md** - Resumen técnico

---

## 💡 Tips útiles

1. **Guardar credenciales de SQL Server**: Usa Windows Authentication si es posible
2. **Crear usuario admin**: 
   ```powershell
   python manage.py createsuperuser
   ```
3. **Ver logs de BD**: Activa DEBUG=True en .env
4. **Usar otra terminal**: El servidor bloquea la terminal, abre otra nueva para comandos

---

## 🎓 Próximos Pasos

Una vez que el servidor está corriendo:

1. **Crear categorías** vía Swagger UI
2. **Agregar especies** con datos reales
3. **Explorar filtrados** (búsqueda, riesgo, endemismo)
4. **Revisar código** y personalizar según necesidades

---

## 📞 Ayuda

Si tienes problemas:
1. Revisa ENTORNO_NECESARIO.md
2. Verifica que SQL Server está corriendo
3. Confirma credenciales en .env
4. Mira logs del servidor (en la terminal)

---

**Versión**: 1.0.0  
**Última actualización**: 2025-11-26  

¡Feliz desarrollo! 🚀
