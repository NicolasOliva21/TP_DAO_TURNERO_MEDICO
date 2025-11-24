# Sistema de Gestión de Turnos Médicos

## Descripción
Sistema profesional de gestión de turnos médicos desarrollado con Python, aplicando principios SOLID, patrones de diseño y arquitectura en capas.

## Características Principales

### ✅ Programación Orientada a Objetos (POO)
- Herencia, polimorfismo y encapsulación
- Clases abstractas e interfaces
- Type hints completos

### ✅ Patrones de Diseño Implementados
- **Repository Pattern**: Abstracción de la capa de datos
- **Unit of Work**: Gestión de transacciones
- **Factory Pattern**: Creación de objetos complejos
- **Singleton**: Gestión de configuración y conexión DB
- **Strategy Pattern**: Diferentes estrategias de validación
- **Observer Pattern**: Sistema de notificaciones y recordatorios

### ✅ Persistencia con SQLAlchemy ORM
- Modelo relacional completo
- Migraciones de base de datos
- RelacionesMany-to-Many
- Índices para optimización

### ✅ Arquitectura en 3 Capas
- **Presentación**: Interfaz de usuario con Rich
- **Lógica de Negocio**: Servicios con validaciones complejas
- **Datos**: Repositorios y acceso a BD

## Funcionalidades Principales

### 🏥 Gestión de Pacientes
- Alta de pacientes con validación de datos únicos (DNI, email)
- Validación de formato de email y fecha de nacimiento
- Baja lógica (conserva historial médico)
- Modificación de datos con control de integridad
- Asociación con obras sociales

### 👨‍⚕️ Gestión de Médicos
- Alta de profesionales con matrícula única
- Asociación a múltiples especialidades
- Configuración de horarios de atención
- Baja lógica (conserva turnos pasados)
- Validación de horarios sin superposición

### 🏥 Gestión de Especialidades
- ABM completo de especialidades médicas
- Validación de nombres únicos
- Control de eliminación (no permitir si hay médicos/turnos asociados)

### 📅 Gestión de Turnos
- Registro de turnos con validación anti-solape
- Verificación de disponibilidad médica
- Estados: Pendiente, Confirmado, Cancelado, Asistido, Inasistido
- Modificación y cancelación con validaciones
- Historial completo de turnos por paciente

### 📋 Historia Clínica
- Consultas médicas asociadas a turnos
- Motivo, diagnóstico e indicaciones
- Recetas electrónicas con firma digital
- Items de receta detallados

### 📊 Reportes y Estadísticas
- Listado de turnos por médico y período
- Cantidad de turnos por especialidad
- Pacientes atendidos en rango de fechas
- Gráfico de asistencias vs inasistencias

### 🔔 Recordatorios Automáticos (Opcional)
- Notificaciones por email
- Envío automático 24h antes del turno
- Control de turnos en estado Reservado

## Arquitectura

```
sistema_turnos_medicos/
├── src/
│   ├── domain/              # Entidades del dominio
│   │   ├── paciente.py
│   │   ├── medico.py
│   │   ├── especialidad.py
│   │   ├── turno.py
│   │   ├── consulta.py
│   │   ├── receta.py
│   │   └── recordatorio.py
│   ├── repositories/        # Capa de persistencia
│   │   ├── base_repository.py
│   │   ├── paciente_repository.py
│   │   ├── medico_repository.py
│   │   ├── turno_repository.py
│   │   └── unit_of_work.py
│   ├── services/            # Lógica de negocio
│   │   ├── paciente_service.py
│   │   ├── medico_service.py
│   │   ├── turno_service.py
│   │   └── reporte_service.py
│   ├── ui/                  # Interfaz de usuario
│   │   ├── paciente_menu.py
│   │   ├── medico_menu.py
│   │   ├── turno_menu.py
│   │   └── reporte_menu.py
│   ├── config/              # Configuración
│   └── utils/               # Utilidades
├── tests/                   # Tests unitarios
├── data/                    # Base de datos
└── main.py                  # Punto de entrada
```

## Modelo de Datos

El sistema gestiona:
- **Pacientes**: Datos personales, obra social, historial
- **Médicos**: Datos profesionales, matrícula, especialidades
- **Especialidades**: Categorías médicas
- **Turnos**: Reservas con validación anti-solape
- **Consultas**: Historial clínico
- **Recetas**: Prescripciones médicas electrónicas
- **Recordatorios**: Notificaciones automáticas
- **Disponibilidad**: Horarios de atención médica
- **Bloqueos**: Períodos no disponibles

## Validaciones Implementadas

### Pacientes
- ✅ DNI y email únicos
- ✅ Formato de email válido
- ✅ Fecha de nacimiento no futura
- ✅ Campos obligatorios no vacíos
- ✅ No baja si tiene turnos futuros

### Médicos
- ✅ Matrícula profesional única
- ✅ Horarios válidos (inicio < fin)
- ✅ Al menos una especialidad asociada
- ✅ No baja si tiene turnos pendientes
- ✅ Validación de superposición de horarios

### Turnos
- ✅ Verificación de disponibilidad médica
- ✅ Anti-solape de turnos (médico y paciente)
- ✅ Fecha futura obligatoria
- ✅ Control de estados (flujo de vida del turno)
- ✅ Validación de duración

### Recetas
- ✅ Solo para turnos atendidos
- ✅ Firma digital del médico
- ✅ Estados: Activa, Anulada, Expirada

## Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

## Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje principal
- **SQLAlchemy 2.0**: ORM para persistencia
- **Pydantic**: Validación de datos
- **Rich**: Interfaz de usuario elegante en consola
- **SQLite**: Base de datos (fácilmente migrable a PostgreSQL/MySQL)

## Autores
Grupo 42: Oliva, Abadía, Giménez

## Fecha
Noviembre 2025
