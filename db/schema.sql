CREATE TABLE Categoria (
    id_categoria INT IDENTITY(1,1),
    nombre NVARCHAR(50) NOT NULL UNIQUE,
    descripcion NVARCHAR(500),
CONSTRAINT pk_categoria PRIMARY KEY (id_categoria),
CONSTRAINT chk_nombre CHECK (nombre IN (N'Aves', N'Mamíferos', N'Reptiles', N'Peces marinos', N'Equinodermos', N'Anfibios'))
)
GO

CREATE TABLE Animal (
    id_animal INT IDENTITY(1,1),
    nombre_comun NVARCHAR(200) NOT NULL,
    nombre_cientifico NVARCHAR(200) NOT NULL UNIQUE,
    descripcion NVARCHAR(MAX),
    habitat NVARCHAR(MAX),
    distribucion NVARCHAR(MAX),
    importancia_ecologica NVARCHAR(MAX),
    estado NVARCHAR(50),
    id_categoria INT NOT NULL,
CONSTRAINT pk_animal PRIMARY KEY (id_animal),
CONSTRAINT fk_animal FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria),
CONSTRAINT chk_estado CHECK (estado IN (N'Preocupación menor (LC)', N'Casi amenazado (NT)', N'Vulnerable (VU)', N'En peligro (EN)', N'Peligro crítico (CR)'))
)
GO

CREATE TABLE FotoAnimal (
  id_foto INT IDENTITY (1,1),
  id_animal INT NOT NULL,
  url_foto NVARCHAR (500) NOT NULL,
  descripcion NVARCHAR (500),

CONSTRAINT pk_foto_animal PRIMARY KEY (id_foto),
CONSTRAINT fk_foto_animal FOREIGN KEY (id_animal) REFERENCES Animal (id_animal)
)
GO

CREATE TABLE Amenaza (
  id_amenaza INT IDENTITY (1,1),
  nombre NVARCHAR (100) NOT NULL UNIQUE,
  descripcion NVARCHAR(MAX),

CONSTRAINT pk_amenaza PRIMARY KEY (id_amenaza)
)
GO

CREATE TABLE AnimalAmenaza (
  id_animal INT NOT NULL,
  id_amenaza INT NOT NULL,

CONSTRAINT pk_animal_amenaza PRIMARY KEY (id_animal, id_amenaza),
CONSTRAINT fk_animal_amenaza_1 FOREIGN KEY (id_animal) REFERENCES Animal (id_animal),
CONSTRAINT fk_animal_amenaza_2 FOREIGN KEY (id_amenaza) REFERENCES Amenaza (id_amenaza)
)
GO

CREATE TABLE AccionProteccion (
  id_accion INT IDENTITY (1,1),
  titulo NVARCHAR (200) NOT NULL,
  descripcion NVARCHAR(MAX) NOT NULL,

CONSTRAINT pk_accion_proteccion PRIMARY KEY (id_accion)
)
GO

CREATE TABLE AnimalAccionProteccion (
  id_animal INT NOT NULL,
  id_accion INT NOT NULL,

CONSTRAINT pk_animal_accion_proteccion PRIMARY KEY (id_animal, id_accion),
CONSTRAINT fk_animal_accion_proteccion_1 FOREIGN KEY (id_animal) REFERENCES Animal (id_animal),
CONSTRAINT fk_animal_accion_proteccion_2 FOREIGN KEY (id_accion) REFERENCES AccionProteccion (id_accion)
)
GO

CREATE TABLE Flora (
  id_planta INT IDENTITY (1,1),
  nombre_comun NVARCHAR (200) NOT NULL,
  nombre_cientifico NVARCHAR (200) NOT NULL,
  descripcion NVARCHAR(MAX),
  distribucion NVARCHAR(MAX),
  estado NVARCHAR (50),

CONSTRAINT pk_flora PRIMARY KEY (id_planta),
CONSTRAINT chk_estado_planta CHECK (estado IN (N'Preocupación menor (LC)', N'Vulnerable (VU)', N'En peligro (EN)', N'Peligro crítico (CR)'))
)
GO

CREATE TABLE FotoFlora (
  id_foto INT IDENTITY (1,1),
  id_planta INT NOT NULL,
  url_foto NVARCHAR (500) NOT NULL,
  descripcion NVARCHAR (500),

CONSTRAINT pk_foto_flora PRIMARY KEY (id_foto),
CONSTRAINT fk_foto_flora FOREIGN KEY (id_planta) REFERENCES Flora (id_planta)
)
GO

CREATE TABLE UsuarioS (
    id_usuario INT IDENTITY(1,1),
    nombre NVARCHAR(150) NOT NULL,
    email NVARCHAR(200) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    fecha_registro DATETIME DEFAULT GETDATE(),
    rol NVARCHAR(20) NOT NULL,
    puntaje INT DEFAULT 0,

CONSTRAINT pk_usuarios PRIMARY KEY (id_usuario),
CONSTRAINT chk_rol CHECK (rol IN (N'admin', N'usuario'))
)
GO

CREATE TABLE ComentarioAnimal (
    id_comentario INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_animal INT NOT NULL,
    contenido NVARCHAR(MAX) NOT NULL,
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_usuario) REFERENCES UsuarioS(id_usuario),
    FOREIGN KEY (id_animal) REFERENCES Animal(id_animal)
)
GO

CREATE TABLE ComentarioPlanta (
    id_comentario INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_planta INT NOT NULL,
    contenido NVARCHAR(MAX) NOT NULL,
    fecha DATETIME DEFAULT GETDATE(),

CONSTRAINT fk_comentario_planta_1 FOREIGN KEY (id_usuario) REFERENCES UsuarioS (id_usuario),
CONSTRAINT fk_comentario_planta_2 FOREIGN KEY (id_planta) REFERENCES Flora (id_planta)
)
GO