-- =============================================================================
-- UPDATE IMAGES - Actualización de URLs de fotos de fauna
-- Fecha: 2024-12-08
-- Descripción: Actualiza las URLs de las fotos de las siguientes especies
-- =============================================================================
-- INSTRUCCIONES:
-- Ejecutar este script en el contenedor SQL Server con:
--   .\scripts\run_sql_update.ps1
-- O manualmente:
--   docker exec ecoalbum-sqlserver /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P "TU_PASSWORD" -d SOMETEDERA -C -i /tmp/update_images.sql
-- =============================================================================

-- Guacamaya Azul Amarilla
UPDATE f 
SET f.url_foto = N'https://cdn.download.ams.birds.cornell.edu/api/v2/asset/58162541/900' 
FROM FotoAnimal f 
JOIN Animal a ON f.id_animal = a.id_animal 
WHERE a.nombre_comun LIKE N'%Guacamaya Azul%';

-- Guacamaya Roja
UPDATE f 
SET f.url_foto = N'https://cdn.download.ams.birds.cornell.edu/api/v2/asset/58146471/1200' 
FROM FotoAnimal f 
JOIN Animal a ON f.id_animal = a.id_animal 
WHERE a.nombre_comun LIKE N'%Guacamaya Roja%';

-- Perico de Azuero o Perico Carato
UPDATE f 
SET f.url_foto = N'https://cdn.download.ams.birds.cornell.edu/api/v1/asset/642285707/320' 
FROM FotoAnimal f 
JOIN Animal a ON f.id_animal = a.id_animal 
WHERE a.nombre_comun LIKE N'%Perico de Azuero%' OR a.nombre_comun LIKE N'%Perico Carato%';

-- Tiburón Martillo Gigante
UPDATE f 
SET f.url_foto = N'https://cdn0.expertoanimal.com/es/razas/8/1/8/tiburon-martillo-gigante_818_0_600.jpg' 
FROM FotoAnimal f 
JOIN Animal a ON f.id_animal = a.id_animal 
WHERE a.nombre_comun LIKE N'%Martillo Gigante%';

-- Tiburón Martillo Común
UPDATE f 
SET f.url_foto = N'https://i.redd.it/ta9fpn4qp3qa1.png' 
FROM FotoAnimal f 
JOIN Animal a ON f.id_animal = a.id_animal 
WHERE a.nombre_comun LIKE N'%Martillo Com%n%';

-- Tortuga Baula o Laúd
UPDATE f 
SET f.url_foto = N'https://img1.wsimg.com/isteam/ip/b3c70235-12b7-463c-b0eb-b033222ea800/anidacion-de-la-tortuga-laud.jpeg' 
FROM FotoAnimal f 
JOIN Animal a ON f.id_animal = a.id_animal 
WHERE a.nombre_comun LIKE N'%Baula%' OR a.nombre_comun LIKE N'%Laúd%';

-- Tortuga Carey
UPDATE f 
SET f.url_foto = N'https://inaturalist-open-data.s3.amazonaws.com/photos/9696845/large.jpg' 
FROM FotoAnimal f 
JOIN Animal a ON f.id_animal = a.id_animal 
WHERE a.nombre_comun LIKE N'%carey%';

-- Tucán Pico Iris
UPDATE f 
SET f.url_foto = N'https://cdn.download.ams.birds.cornell.edu/api/v1/asset/40014881/320' 
FROM FotoAnimal f 
JOIN Animal a ON f.id_animal = a.id_animal 
WHERE a.nombre_comun LIKE N'%Pico Iris%';

-- Verificar cambios
PRINT '=== FOTOS ACTUALIZADAS ===';
SELECT a.nombre_comun, f.url_foto 
FROM FotoAnimal f 
JOIN Animal a ON f.id_animal = a.id_animal 
WHERE a.nombre_comun LIKE N'%Guacamaya%' 
   OR a.nombre_comun LIKE N'%Perico%Azuero%' 
   OR a.nombre_comun LIKE N'%Perico Carato%' 
   OR a.nombre_comun LIKE N'%Martillo%' 
   OR a.nombre_comun LIKE N'%Baula%' 
   OR a.nombre_comun LIKE N'%Laúd%'
   OR a.nombre_comun LIKE N'%Carey%' 
   OR a.nombre_comun LIKE N'%Pico Iris%';
