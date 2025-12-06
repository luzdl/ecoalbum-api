# EcoAlbum API

REST API para gestión de catálogo de especies de Panamá, construida con Django REST Framework y SQL Server.

## 🚀 Inicio Rápido (Docker)

### Prerrequisitos
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado y corriendo

### Pasos

```powershell
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/ecoalbum-api.git
cd ecoalbum-api

# 2. Copiar archivo de configuración
copy .env.example .env

# 3. Iniciar (Docker hace todo automáticamente)
docker-compose up -d

# 4. Esperar ~90 segundos y acceder a:
#    http://localhost:8000/api/swagger/
```

### URLs Disponibles

| Recurso | URL |
|---------|-----|
| 📖 Swagger UI | http://localhost:8000/api/swagger/ |
| 📚 ReDoc | http://localhost:8000/api/docs/ |
| 🏥 Health Check | http://localhost:8000/api/health/ |
| 🦁 Fauna API | http://localhost:8000/api/fauna/ |
| 🌿 Flora API | http://localhost:8000/api/flora/ |
| 🖼️ Galería API | http://localhost:8000/api/galeria/ |

### Comandos Útiles

```powershell
# Ver logs en tiempo real
docker-compose logs -f api

# Ver estado de los contenedores
docker-compose ps

# Reiniciar la API
docker-compose restart api

# Detener todo
docker-compose down

# Reiniciar con datos limpios (borra la BD)
docker-compose down -v && docker-compose up -d
```

---

## 📋 Descripción

EcoAlbum API proporciona endpoints RESTful para consultar un catálogo de especies (fauna y flora) de Panamá. Incluye información sobre estado de conservación IUCN y datos específicos de cada especie.

## ✅ Características

- REST API completa con Django REST Framework
- Base de datos SQL Server con datos precargados (seeding automático)
- Documentación interactiva con Swagger/OpenAPI
- Filtrado avanzado (búsqueda, categoría, estado de conservación)
- Health check endpoint
- CORS habilitado
- Dockerizado para fácil despliegue

## 🛠️ Stack Tecnológico

| Tecnología | Versión |
|-----------|---------|
| Python | 3.12 |
| Django | 5.0+ |
| Django REST Framework | 3.14+ |
| SQL Server | 2022 |
| Docker | Latest |

---

## 📡 Endpoints de la API

### Fauna (Animales)

```bash
# Listar todos los animales
GET /api/fauna/

# Búsqueda por nombre
GET /api/fauna/?q=aguila

# Filtrar por categoría
GET /api/fauna/?categoria=1

# Filtrar por estado de conservación
GET /api/fauna/?estado=Vulnerable

# Detalle de un animal
GET /api/fauna/{id}/

# Fotos de un animal
GET /api/fauna/{id}/fotos/

# Amenazas de un animal
GET /api/fauna/{id}/amenazas/

# Acciones de protección
GET /api/fauna/{id}/acciones/
```

### Flora (Plantas)

```bash
# Listar todas las plantas
GET /api/flora/

# Búsqueda y filtros
GET /api/flora/?q=orquidea

# Detalle de una planta
GET /api/flora/{id}/

# Fotos de una planta
GET /api/flora/{id}/fotos/
```

### Catálogos

```bash
# Categorías de fauna
GET /api/fauna/categorias/

# Amenazas
GET /api/fauna/amenazas/

# Acciones de protección
GET /api/fauna/acciones-proteccion/
```

### Galería

```bash
# Fotos destacadas
GET /api/galeria/destacados/?limit=10

# Fotos aleatorias
GET /api/galeria/aleatorios/?limit=10&tipo=fauna

# Estadísticas
GET /api/galeria/estadisticas/
```

---

## 📁 Estructura del Proyecto

```
ecoalbum-api/
├── apps/
│   ├── core/              # Health check
│   ├── fauna/             # API de fauna (animales)
│   ├── flora/             # API de flora (plantas)
│   └── galeria/           # API de galería
├── db/
│   ├── schema.sql         # Esquema de referencia
│   └── seed.sql           # Datos iniciales
├── ecoalbum_api/          # Configuración Django
├── scripts/
│   ├── wait-for-db.py     # Esperar BD en Docker
│   └── seed-db.py         # Seeding automático
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔧 Desarrollo Local (Sin Docker)

Si prefieres desarrollar sin Docker:

### Prerrequisitos
- Python 3.12+
- SQL Server 2019+ (local o remoto)
- ODBC Driver 18 para SQL Server

### Instalación

```powershell
# 1. Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales de SQL Server

# 4. Ejecutar migraciones
python manage.py migrate

# 5. Iniciar servidor
python manage.py runserver
```

---

## 🐛 Troubleshooting

### El contenedor de SQL Server no inicia
```powershell
# Ver logs de SQL Server
docker-compose logs sqlserver
```

### La API no responde
```powershell
# Verificar que los contenedores estén corriendo
docker-compose ps

# Ver logs de la API
docker-compose logs api
```

### Error de conexión a la base de datos
```powershell
# Reiniciar todo desde cero
docker-compose down -v
docker-compose up -d
```

### Puerto 8000 en uso
```powershell
# Cambiar el puerto en docker-compose.yml
# O detener el proceso que usa el puerto
netstat -ano | findstr :8000
```

---

## 👥 Contribuir

1. Fork el repositorio
2. Crear rama para feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abrir Pull Request

---

## 📄 Licencia

Este proyecto está bajo licencia MIT.

---

**Última actualización**: Diciembre 2024  
**Versión**: 2.0.0