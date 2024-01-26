create database aplicacion;
use aplicacion;

#Tabla usuarios con acceso a app
create table administrador (
	id int primary key auto_increment,
    usuario varchar(20) not null,
    clave varchar(20) not null
);

INSERT INTO administrador (usuario, clave) values
('fernando','123456a');


#Tabla usuarios
CREATE TABLE usuarios (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    documentacion VARCHAR(9) UNIQUE NOT NULL,
    fecha_nacimiento date not null,
    genero ENUM('M', 'F') NOT NULL,
    correo VARCHAR(50) NOT NULL,
    institucion VARCHAR(50) NOT NULL,
    cargo ENUM('Coordinador', 'Profesor', 'Tutor') NOT NULL,
    telefono VARCHAR(25) NOT NULL,
    direccion VARCHAR(150) NOT NULL,
    direccionp VARCHAR(150) NOT NULL
);


