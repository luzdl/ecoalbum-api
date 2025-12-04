# 🐳 EcoAlbum API - Guía Docker

## Requisitos Previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado
- Git para clonar el repositorio

---

## 🚀 Inicio Rápido (Para tus compañeros)

### 1. Clonar el repositorio

```bash
git clone https://github.com/luzdl/ecoalbum-api.git
cd ecoalbum-api
```

### 2. Configurar variables de entorno

```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tus valores (o usar los de ejemplo para desarrollo)
notepad .env  # Windows
nano .env     # Linux/Mac
```

### 3. Iniciar los contenedores

```bash
# Modo producción (en segundo plano)
docker-compose up -d

# O modo desarrollo (con hot-reload)
docker-compose -f docker-compose.dev.yml up
```

### 4. ¡Listo!

- **API**: http://localhost:8000/api/
- **Swagger**: http://localhost:8000/api/swagger/
- **Health Check**: http://localhost:8000/api/health/

---

## 📋 Comandos Útiles

### Gestión de Contenedores

```bash
# Ver contenedores corriendo
docker-compose ps

# Ver logs de la API
docker-compose logs -f api

# Ver logs de SQL Server
docker-compose logs -f sqlserver

# Detener contenedores
docker-compose down

# Detener y eliminar volúmenes (¡borra datos!)
docker-compose down -v

# Reconstruir imágenes
docker-compose build --no-cache
```

### Django dentro del contenedor

```bash
# Ejecutar migraciones
docker-compose exec api python manage.py migrate

# Crear superusuario
docker-compose exec api python manage.py createsuperuser

# Shell de Django
docker-compose exec api python manage.py shell

# Collectstatic (producción)
docker-compose exec api python manage.py collectstatic --noinput
```

### SQL Server dentro del contenedor

```bash
# Conectarse a SQL Server
docker-compose exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "TuPassword" -C

# Ejecutar query
docker-compose exec sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "TuPassword" -C -Q "SELECT name FROM sys.databases"
```

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    docker-compose up                         │
│                                                             │
│  ┌─────────────────────┐         ┌─────────────────────┐   │
│  │   ecoalbum-api      │  ──────▶│   sqlserver         │   │
│  │   (Django/DRF)      │   SQL   │   (MSSQL 2022)      │   │
│  │   :8000             │         │   :1433             │   │
│  └─────────────────────┘         └─────────────────────┘   │
│           │                              │                  │
│           ▼                              ▼                  │
│   ┌───────────────┐              ┌───────────────┐         │
│   │ static_files  │              │ sqlserver_data│         │
│   │ (volumen)     │              │ (volumen)     │         │
│   └───────────────┘              └───────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Configuración de Variables de Entorno

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `DB_ENGINE` | Motor de BD | `mssql` |
| `DB_NAME` | Nombre de la BD | `ecoalbum_db` |
| `DB_HOST` | Host (local o contenedor) | `localhost` o `sqlserver` |
| `DB_PORT` | Puerto SQL Server | `1433` |
| `DB_USER` | Usuario BD | `sa` |
| `DB_PASSWORD` | Contraseña BD | `MiPassword123!` |
| `SECRET_KEY` | Clave secreta Django | `tu-clave-secreta` |
| `DEBUG` | Modo debug | `True` o `False` |
| `ALLOWED_HOSTS` | Hosts permitidos | `*` o `localhost,api.ejemplo.com` |
| `CORS_ALLOW_ALL` | CORS abierto | `True` o `False` |

---

## 🐛 Solución de Problemas

### Error: Puerto 1433 en uso

```bash
# Detener SQL Server local (Windows)
net stop MSSQLSERVER

# O cambiar el puerto en docker-compose.yml
ports:
  - "1434:1433"  # Usar puerto 1434 en host
```

### Error: Contenedor no inicia

```bash
# Ver logs detallados
docker-compose logs --tail=100

# Reiniciar desde cero
docker-compose down -v
docker-compose up --build
```

### Error: Permisos en Linux

```bash
# Dar permisos al script
chmod +x scripts/wait-for-db.py
```

---

## 📦 Despliegue en Producción

Para producción, considera:

1. Usar imágenes específicas con tags de versión
2. Configurar `DEBUG=False`
3. Usar HTTPS con un proxy reverso (nginx/traefik)
4. Configurar backups automáticos del volumen de SQL Server
5. Usar Docker Secrets para las contraseñas

```bash
# Ejemplo con variables de producción
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 🤝 Contribuir

1. Fork el repositorio
2. Crea tu rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Agregar nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request
