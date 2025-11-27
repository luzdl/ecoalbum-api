CREATE TABLE Categoria (
    id_categoria INT IDENTITY(1,1),
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255),
CONSTRAINT pk_categoria PRIMARY KEY (id_categoria),
CONSTRAINT chk_nombre CHECK (nombre IN ('Aves', 'Mamíferos', 'Reptiles', 'Peces marinos', 'Equinodermos', 'Anfibios'))
)

CREATE TABLE Animal (
    id_animal INT IDENTITY(1,1),
    nombre_comun VARCHAR(200) NOT NULL,
    nombre_cientifico VARCHAR(200) NOT NULL UNIQUE,
    descripcion TEXT,
    habitat TEXT,
    distribucion TEXT,
    importancia_ecologica TEXT,
    estado VARCHAR(50),
    id_categoria INT NOT NULL,
CONSTRAINT pk_animal PRIMARY KEY (id_animal),
CONSTRAINT fk_animal FOREIGN KEY (id_categoria) REFERENCES Categoria(id_categoria),
CONSTRAINT chk_estado CHECK (estado IN ('Preocupación menor (LC)', 'Casi amenazado (NT)', 'Vulnerable (VU)', 'En peligro (EN)', 'Peligro crítico (CR)'))
)

CREATE TABLE FotoAnimal (
  id_foto INT IDENTITY (1,1),
  id_animal INT NOT NULL,
  url_foto VARCHAR (500) NOT NULL,
  descripcion VARCHAR (255),

CONSTRAINT pk_foto_animal PRIMARY KEY (id_foto),
CONSTRAINT fk_foto_animal FOREIGN KEY (id_animal) REFERENCES Animal (id_animal),
)

CREATE TABLE Amenaza (
  id_amenaza INT IDENTITY (1,1),
  nombre VARCHAR (100) NOT NULL UNIQUE,
  descripcion TEXT,

CONSTRAINT pk_amenaza PRIMARY KEY (id_amenaza)
)

CREATE TABLE AnimalAmenaza (
  id_animal INT NOT NULL,
  id_amenaza INT NOT NULL,

CONSTRAINT pk_animal_amenaza PRIMARY KEY (id_animal, id_amenaza),
CONSTRAINT fk_animal_amenaza_1 FOREIGN KEY (id_animal) REFERENCES Animal (id_animal),
CONSTRAINT fk_animal_amenaza_2 FOREIGN KEY (id_amenaza) REFERENCES Amenaza (id_amenaza)
)

CREATE TABLE AccionProteccion (
  id_accion INT IDENTITY (1,1),
  titulo VARCHAR (200) NOT NULL,
  descripcion TEXT NOT NULL,

CONSTRAINT pk_accion_proteccion PRIMARY KEY (id_accion)
)

CREATE TABLE AnimalAccionProteccion (
  id_animal INT NOT NULL,
  id_accion INT NOT NULL,

CONSTRAINT pk_animal_accion_proteccion PRIMARY KEY (id_animal, id_accion),
CONSTRAINT fk_animal_accion_proteccion_1 FOREIGN KEY (id_animal) REFERENCES Animal (id_animal),
CONSTRAINT fk_animal_accion_proteccion_2 FOREIGN KEY (id_accion) REFERENCES AccionProteccion (id_accion)
)

CREATE TABLE Flora (
  id_planta INT IDENTITY (1,1),
  nombre_comun VARCHAR (200) NOT NULL,
  nombre_cientifico VARCHAR (200) NOT NULL,
  descripcion TEXT,
  distribucion TEXT,
  estado VARCHAR (50),

CONSTRAINT pk_flora PRIMARY KEY (id_planta),
CONSTRAINT chk_estado_planta CHECK (estado IN ('Preocupación menor (LC)', 'Vulnerable (VU)', 'En peligro (EN)', 'Peligro crítico (CR)'))
)

CREATE TABLE FotoFlora (
  id_foto INT IDENTITY (1,1),
  id_planta INT NOT NULL,
  url_foto VARCHAR (500) NOT NULL,
  descripcion VARCHAR (255),

CONSTRAINT pk_foto_flora PRIMARY KEY (id_foto),
CONSTRAINT fk_foto_flora FOREIGN KEY (id_planta) REFERENCES Flora (id_planta)
)

CREATE TABLE UsuarioS (
    id_usuario INT IDENTITY(1,1),
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(200) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,   -- la contraseña va en hash
    fecha_registro DATETIME DEFAULT GETDATE(),
    rol VARCHAR(20) NOT NULL,
    puntaje INT DEFAULT 0,

CONSTRAINT pk_usuarios PRIMARY KEY (id_usuario),
CONSTRAINT chk_rol CHECK (rol IN ('admin', 'usuario'))
);

CREATE TABLE ComentarioAnimal (
    id_comentario INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_animal INT NOT NULL,
    contenido TEXT NOT NULL,
    fecha DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (id_usuario) REFERENCES UsuarioS(id_usuario),
    FOREIGN KEY (id_animal) REFERENCES Animal(id_animal)
);

CREATE TABLE ComentarioPlanta (
    id_comentario INT IDENTITY(1,1) PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_planta INT NOT NULL,
    contenido TEXT NOT NULL,
    fecha DATETIME DEFAULT GETDATE(),

CONSTRAINT fk_comentario_planta_1 FOREIGN KEY (id_usuario) REFERENCES UsuarioS (id_usuario),
CONSTRAINT fk_comentario_planta_2 FOREIGN KEY (id_planta) REFERENCES Flora (id_planta)
);