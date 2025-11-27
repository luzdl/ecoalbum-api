# ENTORNO NECESARIO - EcoAlbum API

## Verificación de Requisitos de Sistema

Antes de ejecutar EcoAlbum API, asegúrate de que tu entorno cumple con los siguientes requisitos:

---

## 1. ✅ Python 3.12+ con venv y pip

**Verificar:**
```bash
python --version
pip --version
```

**Esperado:**
- Python 3.12 o superior
- pip incluido

**Instalación (si es necesario):**
- **Windows**: [Descargar Python](https://www.python.org/downloads/)
- **Linux**: `sudo apt-get install python3.12 python3.12-venv python3.12-dev`
- **macOS**: `brew install python@3.12`

---

## 2. ✅ Paquetes del Sistema: msodbcsql18, mssql-tools18, unixodbc-dev, ODBC Driver 18

**Verificar (Linux):**
```bash
dpkg -l | grep msodbcsql
dpkg -l | grep mssql-tools
dpkg -l | grep unixodbc
```

**Instalación (Linux):**
```bash
# Agregar repositorio de Microsoft
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list

# Instalar paquetes
sudo apt-get update
sudo apt-get install msodbcsql18
sudo apt-get install mssql-tools18
sudo apt-get install unixodbc-dev
```

**Instalación (macOS):**
```bash
brew install unixodbc
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install mssql-tools18
```

**Instalación (Windows):**
- Descargar [ODBC Driver 18 para SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- Ejecutar instalador y seguir pasos

---

## 3. ✅ SQL Server Accesible con Credenciales Válidas

**Verificar Conexión (Linux/macOS):**
```bash
sqlcmd -S localhost,1433 -U sa -P 'YourPassword123!' -Q "SELECT @@VERSION"
```

**Requisitos:**
- Microsoft SQL Server 2019 o superior (local o remoto)
- Credenciales válidas (usuario y contraseña)
- Permisos para crear/modificar bases de datos
- Firewall: Puerto 1433 abierto (predeterminado)

**Verificación Rápida:**
```bash
# Prueba de conexión básica
telnet localhost 1433

# O usar sqlcmd
sqlcmd -S your_server,1433 -U your_user -P 'your_password' -Q "SELECT SYSDATETIME()"
```

---

## 4. ✅ Archivo .env con Todas las Variables (sin placeholders)

**Verificar:**
```bash
cat .env | grep -E "DB_|SECRET_|DEBUG|ALLOWED"
```

**Archivo .env Ejemplo Completado:**
```env
DB_ENGINE=mssql
DB_NAME=ecoalbum_db
DB_HOST=localhost
DB_PORT=1433
DB_USER=sa
DB_PASSWORD=YourSecurePassword123!
SECRET_KEY=django-insecure-abcdef123456ghijkl789mnopqrs
DEBUG=True
ALLOWED_HOSTS=*
CORS_ALLOW_ALL=True
API_URL=http://localhost:8000/api
```

**Generar SECRET_KEY:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

---

## 5. ✅ Puerto 8000 Accesible (no bloqueado por firewall)

**Verificar:**
```bash
# Linux/macOS
netstat -tuln | grep 8000
lsof -i :8000

# Windows
netstat -ano | find ":8000"
```

**Si está ocupado, especificar otro puerto:**
```bash
python manage.py runserver 0.0.0.0:8001
```

**Permitir en firewall:**
```bash
# Linux (ufw)
sudo ufw allow 8000/tcp

# macOS (PF - si está habilitado)
echo 'pass in on lo0 proto tcp from any to 127.0.0.1 port 8000' | sudo pfctl -ef -

# Windows
netsh advfirewall firewall add rule name="Django API" dir=in action=allow protocol=tcp localport=8000
```

---

## 6. ✅ Comandos de Inicio

**Primer inicio (setup completo):**
```bash
# 1. Clonar/descargar repositorio
cd ecoalbum-api

# 2. Ejecutar setup
bash scripts/dev_setup.sh

# Este script:
# - Crea venv
# - Instala dependencias
# - Genera SECRET_KEY
# - Ejecuta migraciones
```

**Inicios posteriores:**
```bash
bash scripts/run_api.sh
```

**Pasos manuales (si necesario):**
```bash
# Activar venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

---

## 7. ✅ Verificación de Funcionamiento

**Health Check (API activa):**
```bash
curl http://localhost:8000/api/health/
```

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-26T10:30:45.123456Z",
  "message": "All systems operational"
}
```

**Swagger UI:**
```
http://localhost:8000/api/swagger/
```

**Crear categoria de prueba:**
```bash
curl -X POST http://localhost:8000/api/categories/ \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","description":"Test category"}'
```

---

## Checklist de Configuración Completa

Antes de ejecutar el servidor, completa este checklist:

```
☐ Python 3.12 instalado y verificado
☐ pip actualizado (pip install --upgrade pip)
☐ ODBC Driver 18 instalado
☐ SQL Server accesible y credenciales validadas
☐ msodbcsql18 y mssql-tools18 instalados (Linux/macOS)
☐ Archivo .env creado con variables completadas (sin placeholders)
☐ Base de datos creada en SQL Server
☐ Puerto 8000 disponible y firewall permitido
☐ Repositorio clonado en directorio local
☐ script dev_setup.sh ejecutado exitosamente
☐ curl http://localhost:8000/api/health/ retorna status: "healthy"
☐ Swagger UI accesible en http://localhost:8000/api/swagger/
```

---

## Troubleshooting Rápido

| Problema | Solución |
|----------|----------|
| Import error: mssql_django | `pip install mssql-django` |
| ODBC Driver not found | Instalar ODBC Driver 18 (ver paso 2) |
| Connection refused (database) | Verificar SQL Server está corriendo y credenciales |
| Port 8000 in use | Usar: `python manage.py runserver 0.0.0.0:8001` |
| Migrations failed | Ejecutar: `python manage.py migrate --run-syncdb` |
| SECRET_KEY error | Generar: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |

---

## Recursos de Ayuda

- [Django Official Docs](https://docs.djangoproject.com/)
- [mssql-django GitHub](https://github.com/microsoft/mssql-django)
- [ODBC Driver Installation](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- [SQL Server Tools](https://learn.microsoft.com/en-us/sql/tools/sqlcmd-utility)

---

**Generado**: 2025-11-26  
**Versión**: 1.0.0  
**Estado**: ✅ LISTO PARA USAR
