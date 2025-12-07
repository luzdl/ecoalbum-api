# Dockerfile para EcoAlbum API
# Multi-stage build para optimizar el tamaño de la imagen

# ============================================
# Stage 1: Base con dependencias del sistema
# ============================================
FROM python:3.12-slim as base

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema para MSSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    apt-transport-https \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64,arm64,armhf signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends \
        msodbcsql18 \
        mssql-tools18 \
        unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Agregar sqlcmd al PATH
ENV PATH="$PATH:/opt/mssql-tools18/bin"

# ============================================
# Stage 2: Dependencias de Python
# ============================================
FROM base as dependencies

WORKDIR /app

# Copiar solo requirements para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# ============================================
# Stage 3: Aplicación final
# ============================================
FROM dependencies as production

WORKDIR /app

# Crear usuario no-root para seguridad
RUN addgroup --system --gid 1001 django \
    && adduser --system --uid 1001 --gid 1001 django

# Copiar el código de la aplicación
COPY --chown=django:django . .

# Copiar scripts de utilidades
COPY --chown=django:django scripts/wait-for-db.py /app/scripts/
COPY --chown=django:django scripts/seed-db.py /app/scripts/
COPY --chown=django:django scripts/init-db.py /app/scripts/

# Crear directorio para archivos estáticos
RUN mkdir -p /app/staticfiles && chown django:django /app/staticfiles

# Cambiar al usuario no-root
USER django

# Puerto de la aplicación
EXPOSE 8000

# Comando por defecto - Ejecuta schema.sql primero, luego fake migrate, luego seed
CMD ["sh", "-c", "python scripts/wait-for-db.py && python scripts/init-db.py && python manage.py runserver 0.0.0.0:8000"]
