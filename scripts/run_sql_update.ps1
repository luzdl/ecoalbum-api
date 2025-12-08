<#
.SYNOPSIS
    Ejecuta scripts SQL de actualización en el contenedor SQL Server.

.DESCRIPTION
    Este script copia un archivo .sql al contenedor SQL Server y lo ejecuta.
    Lee las credenciales del archivo .env automáticamente.

.PARAMETER SqlFile
    Ruta al archivo SQL a ejecutar. Por defecto: db/updates/update_images.sql

.EXAMPLE
    .\scripts\run_sql_update.ps1
    .\scripts\run_sql_update.ps1 -SqlFile "db/updates/otro_script.sql"
#>

param(
    [string]$SqlFile = "db/updates/update_images.sql",
    [string]$ContainerName = "ecoalbum-sqlserver"
)

# Colores para output
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Success { param($msg) Write-Host "[OK] $msg" -ForegroundColor Green }
function Write-Err { param($msg) Write-Host "[ERROR] $msg" -ForegroundColor Red }

# Obtener directorio del script
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir

# Leer .env
$EnvFile = Join-Path $ProjectRoot ".env"
if (-not (Test-Path $EnvFile)) {
    Write-Err "No se encontró el archivo .env en $ProjectRoot"
    exit 1
}

# Parsear .env
$envContent = Get-Content $EnvFile
$DB_PASSWORD = ($envContent | Where-Object { $_ -match "^DB_PASSWORD=" }) -replace "DB_PASSWORD=", ""
$DB_NAME = ($envContent | Where-Object { $_ -match "^DB_NAME=" }) -replace "DB_NAME=", ""

if (-not $DB_PASSWORD -or -not $DB_NAME) {
    Write-Err "No se pudo leer DB_PASSWORD o DB_NAME del .env"
    exit 1
}

# Verificar archivo SQL
$SqlFilePath = Join-Path $ProjectRoot $SqlFile
if (-not (Test-Path $SqlFilePath)) {
    Write-Err "No existe el archivo SQL: $SqlFilePath"
    exit 1
}

Write-Info "Archivo SQL: $SqlFile"
Write-Info "Base de datos: $DB_NAME"
Write-Info "Contenedor: $ContainerName"

# Verificar que el contenedor está corriendo
$containerStatus = docker ps --filter "name=$ContainerName" --format "{{.Status}}" 2>$null
if (-not $containerStatus) {
    Write-Err "El contenedor '$ContainerName' no está corriendo. Ejecuta 'docker-compose up -d' primero."
    exit 1
}
Write-Success "Contenedor activo: $containerStatus"

# Copiar SQL al contenedor
Write-Info "Copiando SQL al contenedor..."
docker cp $SqlFilePath "${ContainerName}:/tmp/update_script.sql"
if ($LASTEXITCODE -ne 0) {
    Write-Err "Error al copiar el archivo SQL al contenedor"
    exit 1
}

# Ejecutar SQL
Write-Info "Ejecutando SQL..."
docker exec $ContainerName /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P $DB_PASSWORD -d $DB_NAME -C -i /tmp/update_script.sql

if ($LASTEXITCODE -eq 0) {
    Write-Success "Script SQL ejecutado correctamente!"
} else {
    Write-Err "Error al ejecutar el script SQL"
    exit 1
}

# Limpiar
docker exec $ContainerName rm /tmp/update_script.sql 2>$null

Write-Host ""
Write-Success "Actualización completada. Verifica los cambios en la API."
