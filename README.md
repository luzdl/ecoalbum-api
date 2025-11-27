# EcoAlbum API

REST API para gestión de catálogo de especies de Panamá, construida con Django REST Framework y SQL Server.

## Descripción

EcoAlbum API proporciona endpoints RESTful para consultar y gestionar un catálogo de especies (fauna y flora) de Panamá. Incluye información sobre estado de conservación IUCN, status CITES, y datos específicos de endemismo.

## Características

- ✅ REST API completa con Django REST Framework
- ✅ Soporte para Microsoft SQL Server (MSSQL) con mssql-django
- ✅ Documentación interactiva con Swagger/OpenAPI
- ✅ Filtrado avanzado (búsqueda, categoría, nivel de riesgo, endemismo)
- ✅ Health check endpoint
- ✅ CORS habilitado para desarrollo
- ✅ Tests unitarios incluidos
- ✅ Modelos con enums (RiskLevel IUCN, CITESStatus)

## Stack Tecnológico

| Tecnología | Versión |
|-----------|---------|
| Python | 3.12+ |
| Django | 5.0+ |
| Django REST Framework | 3.14+ |
| mssql-django | 1.4+ |
| pyodbc | 5.1+ |
| drf-yasg (Swagger) | 1.21+ |
| django-filter | 24.1+ |
| django-cors-headers | 4.3+ |

## Requisitos del Sistema

### 1. Python y Entorno Virtual
```bash
python --version  # Debe ser 3.12 o superior
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. SQL Server
- Microsoft SQL Server 2019 o superior
- ODBC Driver 18 para SQL Server instalado
- Usuario con permisos para crear/modificar base de datos

### 3. Paquetes del Sistema (Linux)
```bash
sudo apt-get install msodbcsql18
sudo apt-get install mssql-tools18
sudo apt-get install unixodbc-dev
```

### 4. Paquetes del Sistema (macOS)
```bash
brew install unixodbc
brew install mssql-tools18
```

### 5. Paquetes del Sistema (Windows)
- ODBC Driver 18 para SQL Server: [Descargar](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- SQL Server Native Client (opcional): [Descargar](https://www.microsoft.com/en-us/download/details.aspx?id=50402)

## Instalación

### Paso 1: Clonar el repositorio
```bash
git clone <repository-url>
cd ecoalbum-api
```

### Paso 2: Ejecutar setup de desarrollo
```bash
bash scripts/dev_setup.sh
```

Este script:
- Crea el entorno virtual
- Instala dependencias desde `requirements.txt`
- Genera `SECRET_KEY` automáticamente
- Ejecuta migraciones de base de datos

### Paso 3: Configurar variables de entorno
```bash
cp .env.example .env
```

Edita `.env` con tus credenciales de SQL Server:
```env
DB_ENGINE=mssql
DB_NAME=ecoalbum_db
DB_HOST=localhost
DB_PORT=1433
DB_USER=sa
DB_PASSWORD=YourPassword123!
SECRET_KEY=django-insecure-xxxxxxxxxxxxx
DEBUG=True
ALLOWED_HOSTS=*
CORS_ALLOW_ALL=True
API_URL=http://localhost:8000/api
```

### Paso 4: Crear base de datos (primera vez)
```bash
python manage.py migrate
```

### Paso 5: Crear usuario administrador (opcional)
```bash
python manage.py createsuperuser
```

### Paso 6: Cargar datos iniciales (opcional)
```bash
bash scripts/load_sql.sh
```

## Uso

### Iniciar servidor de desarrollo
```bash
bash scripts/run_api.sh
```

El servidor estará disponible en: `http://localhost:8000/`

### Endpoints Principales

#### Health Check
```bash
curl http://localhost:8000/api/health/
```

#### Listar Categorías
```bash
curl http://localhost:8000/api/categories/
```

#### Buscar Especies
```bash
# Todas las especies
curl http://localhost:8000/api/species/

# Búsqueda por nombre
curl "http://localhost:8000/api/species/?q=harpy"

# Filtrar por nivel de riesgo
curl "http://localhost:8000/api/species/?risk_level=VU"

# Filtrar endémicas
curl "http://localhost:8000/api/species/?endemic=true"

# Combinar filtros
curl "http://localhost:8000/api/species/?q=eagle&risk_level=VU&endemic=true"

# Ordenar resultados
curl "http://localhost:8000/api/species/?ordering=-created_at"
```

#### Detalle de Especie
```bash
curl http://localhost:8000/api/species/1/
```

### Documentación Interactiva

- **Swagger UI**: http://localhost:8000/api/swagger/
- **ReDoc**: http://localhost:8000/api/schema/
- **OpenAPI JSON**: http://localhost:8000/api/schema/openapi.json

## Estructura de Proyecto

```
ecoalbum-api/
├── ecoalbum_api/           # Configuración Django
│   ├── settings.py        # Configuración MSSQL
│   ├── urls.py            # Routing principal
│   ├── wsgi.py            # WSGI para producción
│   └── asgi.py            # ASGI para async
├── apps/
│   ├── core/              # App sistema (health check)
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── services.py
│   │   ├── tests.py
│   │   └── urls.py
│   └── species/           # App catálogo de especies
│       ├── models/
│       │   ├── category.py
│       │   └── species.py
│       ├── serializers/
│       │   ├── category_serializer.py
│       │   └── species_serializer.py
│       ├── views/
│       │   ├── category_view.py
│       │   └── species_view.py
│       ├── filters.py     # Filtrado avanzado
│       ├── services.py    # Lógica de negocio
│       └── tests.py
├── db/
│   ├── schema.sql         # Definición de tablas
│   └── seed.sql           # Datos iniciales
├── scripts/
│   ├── dev_setup.sh       # Setup inicial
│   ├── run_api.sh         # Iniciar servidor
│   └── load_sql.sh        # Cargar SQL
├── docs/
│   └── openapi.yaml       # Especificación OpenAPI
├── manage.py              # CLI Django
├── requirements.txt       # Dependencias Python
├── .env.example           # Variables de entorno (plantilla)
├── .gitignore
└── README.md
```

## Modelos de Datos

### Category
```python
- id: Integer (PK)
- name: String(100) - Único
- description: Text
- created_at: DateTime (auto)
- updated_at: DateTime (auto)
```

### Species
```python
- id: Integer (PK)
- common_name: String(255)
- scientific_name: String(255) - Único
- category: FK → Category
- risk_level: Enum [EX, EW, CR, EN, VU, NT, LC, DD, NE]
- cites_status: Enum [I, II, III, NL]
- image_url: URL (opcional)
- description: Text (opcional)
- endemic: Boolean
- created_at: DateTime (auto)
- updated_at: DateTime (auto)
```

### RiskLevel (IUCN Red List)
- **EX**: Extinct (Extinto)
- **EW**: Extinct in the Wild (Extinto en la Naturaleza)
- **CR**: Critically Endangered (En Peligro Crítico)
- **EN**: Endangered (En Peligro)
- **VU**: Vulnerable
- **NT**: Near Threatened (Casi Amenazado)
- **LC**: Least Concern (Preocupación Menor)
- **DD**: Data Deficient (Datos Insuficientes)
- **NE**: Not Evaluated (No Evaluado)

### CITESStatus
- **I**: Appendix I (Apéndice I)
- **II**: Appendix II (Apéndice II)
- **III**: Appendix III (Apéndice III)
- **NL**: Not Listed (No Listado)

## Parámetros de Filtrado y Búsqueda

### GET /api/species/

| Parámetro | Tipo | Descripción | Ejemplo |
|-----------|------|-------------|---------|
| `q` | string | Búsqueda en nombre común y científico | `?q=harpy` |
| `category` | string | Filtrar por nombre de categoría | `?category=Birds` |
| `risk_level` | string | Filtrar por nivel IUCN | `?risk_level=VU` |
| `endemic` | boolean | Filtrar endémicas | `?endemic=true` |
| `ordering` | string | Ordenar resultados | `?ordering=-created_at` |
| `page` | integer | Número de página | `?page=2` |

### Campos para Ordenamiento
- `common_name`
- `scientific_name`
- `risk_level`
- `created_at`
- `-created_at` (descendente)

## Testing

### Ejecutar tests
```bash
python manage.py test
```

### Ejecutar tests con cobertura
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generar reporte HTML
```

## Variables de Entorno

Ver `.env.example` para template completo. Variables principales:

```env
# Base de Datos
DB_ENGINE=mssql
DB_NAME=ecoalbum_db
DB_HOST=localhost
DB_PORT=1433
DB_USER=sa
DB_PASSWORD=secure_password

# Django
SECRET_KEY=django-insecure-xxx
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# API
CORS_ALLOW_ALL=True
API_URL=http://localhost:8000/api
```

## Troubleshooting

### Error: "No module named 'mssql_django'"
```bash
pip install -r requirements.txt
```

### Error: "ODBC Driver not found"
Asegúrate de que ODBC Driver 18 para SQL Server está instalado:
```bash
# Linux
sudo apt-get install msodbcsql18

# macOS
brew install unixodbc
```

### Error: "Connection to database failed"
Verifica:
1. SQL Server está corriendo
2. Variables de entorno `.env` están correctas
3. Usuario tiene permisos en la base de datos
4. Firewall permite conexión al puerto 1433

### Error: "No such table: species_category"
Ejecuta migraciones:
```bash
python manage.py migrate
```

### Error: "Puerto 8000 en uso"
Especifica otro puerto:
```bash
python manage.py runserver 0.0.0.0:8001
```

## Desarrollo

### Crear nueva migración
```bash
python manage.py makemigrations
python manage.py migrate
```

### Crear superuser
```bash
python manage.py createsuperuser
```

### Entrar a Django admin
```
http://localhost:8000/admin/
```

### Generar datos de prueba
```python
from apps.species.models import Category, Species
from apps.species.services import create_test_data
create_test_data()
```

## Despliegue en Producción

### 1. Preparar entorno
```bash
export DEBUG=False
export SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
```

### 2. Usar gunicorn
```bash
gunicorn ecoalbum_api.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

### 3. Configurar servidor web (Nginx)
```nginx
upstream ecoalbum {
    server localhost:8000;
}

server {
    listen 80;
    server_name api.ecoalbum.com;

    location / {
        proxy_pass http://ecoalbum;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/ecoalbum-api/staticfiles/;
    }
}
```

### 4. Recolectar archivos estáticos
```bash
python manage.py collectstatic --noinput
```

## Contribuir

1. Fork el repositorio
2. Crear rama para feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para detalles.

## Contacto

- **Equipo**: EcoAlbum Team
- **Email**: info@ecoalbum.com
- **Web**: https://ecoalbum.com

## Recursos Adicionales

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [mssql-django Docs](https://github.com/microsoft/mssql-django)
- [IUCN Red List](https://www.iucnredlist.org/)
- [CITES](https://cites.org/)

---

**Última actualización**: 2025-11-26  
**Versión**: 1.0.0