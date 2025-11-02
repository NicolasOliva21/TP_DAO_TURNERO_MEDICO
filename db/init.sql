-- db/init.sql
-- Crea el esquema base acorde a los modelos del backend

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =======================
-- Usuarios (autenticación)
-- =======================
CREATE TABLE IF NOT EXISTS users (
  id               SERIAL PRIMARY KEY,
  email            VARCHAR(120) UNIQUE NOT NULL,
  name             VARCHAR(80)  NOT NULL,
  hashed_password  VARCHAR(255) NOT NULL,
  role             VARCHAR(20)  NOT NULL DEFAULT 'admin'
);

-- =========
-- Pacientes
-- =========
CREATE TABLE IF NOT EXISTS patients (
  id                SERIAL PRIMARY KEY,
  nombre            VARCHAR(80)  NOT NULL,
  apellido          VARCHAR(80)  NOT NULL,
  dni               VARCHAR(20)  NOT NULL,
  fecha_nacimiento  VARCHAR(10)  NOT NULL, -- ISO YYYY-MM-DD (como exige el modelo)
  genero            VARCHAR(20),
  direccion         VARCHAR(120),
  telefono          VARCHAR(30),
  email             VARCHAR(120),
  obra_social       VARCHAR(120),
  nro_afiliado      VARCHAR(50),
  activo            BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS ix_patients_dni ON patients (dni);

-- =======
-- Médicos
-- =======
CREATE TABLE IF NOT EXISTS doctors (
  id         SERIAL PRIMARY KEY,
  nombre     VARCHAR(80)  NOT NULL,
  apellido   VARCHAR(80)  NOT NULL,
  dni        VARCHAR(20)  NOT NULL,
  genero     VARCHAR(20),
  email      VARCHAR(120),
  telefono   VARCHAR(30),
  direccion  VARCHAR(120),
  matricula  VARCHAR(40)  NOT NULL UNIQUE,
  activo     BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE INDEX IF NOT EXISTS ix_doctors_dni ON doctors (dni);

-- =============
-- Especialidades
-- =============
CREATE TABLE IF NOT EXISTS specialties (
  id          SERIAL PRIMARY KEY,
  nombre      VARCHAR(120) NOT NULL UNIQUE,
  descripcion VARCHAR(255),
  activa      BOOLEAN NOT NULL DEFAULT TRUE
);

-- ==========
-- Turnos/HC
-- ==========
-- Estados permitidos: Reservado | Cancelado | Reprogramado | Atendido
CREATE TABLE IF NOT EXISTS appointments (
  id               SERIAL PRIMARY KEY,
  paciente_id      INTEGER NOT NULL REFERENCES patients(id)    ON DELETE RESTRICT,
  medico_id        INTEGER NOT NULL REFERENCES doctors(id)     ON DELETE RESTRICT,
  especialidad_id  INTEGER NOT NULL REFERENCES specialties(id) ON DELETE RESTRICT,
  fecha            VARCHAR(25) NOT NULL,   -- ISO 'YYYY-MM-DDTHH:MM'
  duracion_min     INTEGER NOT NULL DEFAULT 30,
  estado           VARCHAR(20) NOT NULL DEFAULT 'Reservado'
    CHECK (estado IN ('Reservado','Cancelado','Reprogramado','Atendido')),
  receta_url       VARCHAR(255)
);

CREATE INDEX IF NOT EXISTS ix_appointments_medico_fecha
  ON appointments (medico_id, fecha);
CREATE INDEX IF NOT EXISTS ix_appointments_estado
  ON appointments (estado);
