# Sistema de Gestión de Turnos Médicos 🏥

Sistema profesional de gestión de turnos médicos desarrollado con Python, aplicando paradigma orientado a objetos, patrones de diseño y arquitectura en capas.

**Universidad Nacional de Cuyo - Facultad de Ingeniería**  
**Materia**: Diseño y Arquitectura Orientada a Objetos  
**Grupo 42**: Oliva, Abadía, Giménez  
**Año**: 2025

---

## 📋 Descripción

Sistema integral de gestión de turnos médicos que permite:
- Gestión completa de pacientes, médicos y especialidades
- Creación de turnos con validación anti-solapamiento
- Control de disponibilidad y bloqueos de médicos
- Historia clínica y recetas médicas
- Seguimiento de estados de turnos
- Recordatorios automáticos

## 🎯 Objetivos del Proyecto

✅ **Paradigma Orientado a Objetos**: Herencia, polimorfismo, encapsulación  
✅ **Persistencia**: SQLAlchemy ORM 2.0 con SQLite  
✅ **Patrones de Diseño**: Singleton, Repository, Unit of Work, Factory, Strategy  
✅ **Arquitectura en Capas**: Separación clara de responsabilidades  
✅ **Código Profesional**: Type hints, docstrings, manejo de excepciones  

## 🏗️ Arquitectura

### Arquitectura en 3 Capas

```
┌─────────────────────────────────────────┐
│   CAPA DE PRESENTACIÓN (UI)             │
│   - Menús interactivos con Rich         │
│   - Validación de entradas              │
│   - Formateo de salidas                 │
├─────────────────────────────────────────┤
│   CAPA DE LÓGICA DE NEGOCIO (Services) │
│   - TurnoService (anti-solapamiento)    │
│   - Validaciones complejas              │
│   - Reglas de negocio                   │
├─────────────────────────────────────────┤
│   CAPA DE ACCESO A DATOS (Repositories)│
│   - Unit of Work Pattern                │
│   - Repositorios específicos (10)       │
│   - BaseRepository (CRUD genérico)      │
├─────────────────────────────────────────┤
│   CAPA DE DOMINIO (Domain)              │
│   - 11 Entidades con SQLAlchemy         │
│   - Relaciones Many-to-Many             │
│   - Soft Delete + Audit Trail           │
└─────────────────────────────────────────┘
              ↓
    [ SQLite Database ]
```

## 🎨 Patrones de Diseño Implementados

### 1. **Singleton Pattern** ✅
- **Ubicación**: `src/config/settings.py`, `src/repositories/database.py`
- **Propósito**: Una única instancia de configuración y conexión DB
- **Implementación**: Control de instanciación con `__new__`

### 2. **Repository Pattern** ✅
- **Ubicación**: `src/repositories/`
- **Propósito**: Abstracción del acceso a datos
- **Implementación**:
  - `BaseRepository`: CRUD genérico para todas las entidades
  - 10 repositorios específicos con consultas personalizadas

### 3. **Unit of Work Pattern** ✅
- **Ubicación**: `src/repositories/unit_of_work.py`
- **Propósito**: Gestión transaccional y coordinación de repositorios
- **Implementación**: Context manager con commit/rollback automático

### 4. **Factory Pattern** ✅
- **Ubicación**: `src/services/turno_service.py`
- **Propósito**: Creación compleja de turnos con validaciones
- **Implementación**: Método factory con validación de 7 reglas de negocio

### 5. **Strategy Pattern** ✅
- **Ubicación**: Validaciones en servicios
- **Propósito**: Diferentes estrategias de validación intercambiables
- **Implementación**: Validadores de disponibilidad, solapamiento, etc.

### 6. **Template Method Pattern** ✅
- **Ubicación**: `src/repositories/base_repository.py`
- **Propósito**: Definir estructura de operaciones CRUD
- **Implementación**: Métodos comunes que repositorios heredan

## 📦 Modelo de Dominio

### Entidades Principales (11)

1. **Paciente**: DNI único, email único, obra social
2. **Medico**: Matrícula única, múltiples especialidades
3. **Especialidad**: Categorización de servicios
4. **EstadoTurno**: PEND, CONF, CANC, ASIS, INAS
5. **Turno**: Entidad central con anti-solapamiento
6. **DisponibilidadMedico**: Horarios semanales de atención
7. **BloqueoMedico**: Vacaciones, capacitaciones
8. **Consulta**: Historia clínica (1:1 con Turno ASIS)
9. **Receta**: Prescripción médica con firma digital
10. **ItemReceta**: Medicamentos de la receta
11. **Recordatorio**: Notificaciones automáticas

### Relaciones Clave

- **Medico ↔ Especialidad**: Many-to-Many (tabla asociativa `medico_especialidad`)
- **Turno → Paciente**: Many-to-One
- **Turno → Medico**: Many-to-One
- **Turno → Especialidad**: Many-to-One
- **Turno → EstadoTurno**: Many-to-One
- **Consulta → Turno**: One-to-One (solo turnos ASIS)
- **Receta → Consulta**: Many-to-One

## ✅ Validaciones Implementadas

### Validaciones de Turnos (CRÍTICAS)

1. ✅ **Fecha futura obligatoria**
2. ✅ **Verificación de disponibilidad** del médico (día y horario)
3. ✅ **Médico tiene la especialidad** seleccionada
4. ✅ **Anti-solape para el mismo médico** (no dos turnos simultáneos)
5. ✅ **Anti-solape para el mismo paciente** (no dos turnos simultáneos)
6. ✅ **Control de bloqueos** del médico (vacaciones, etc.)
7. ✅ **Estado inicial PEND** (Pendiente)

### Otras Validaciones

- **Paciente**: DNI único, email único y válido, fecha nacimiento no futura
- **Médico**: Matrícula única, al menos una especialidad, DNI y email únicos
- **Especialidad**: Nombre único
- **Consulta**: Solo para turnos ASIS (Asistido)
- **Receta**: Solo para consultas existentes, al menos un medicamento

## 🚀 Instalación y Ejecución

### Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Terminal/PowerShell

### Paso 1: Clonar/Descargar el Proyecto

```bash
cd sistema_turnos_medicos
```

### Paso 2: Crear Entorno Virtual (Recomendado)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar el Sistema

```bash
python main.py
```

### Primera Ejecución

Al ejecutar por primera vez, el sistema:
1. ✅ Crea la base de datos SQLite en `data/turnos_medicos.db`
2. ✅ Crea todas las tablas
3. ✅ Inicializa estados de turno (PEND, CONF, CANC, ASIS, INAS)
4. ✅ Carga datos de ejemplo:
   - 5 Especialidades
   - 3 Médicos con horarios
   - 4 Pacientes

## 📖 Uso del Sistema

### Menú Principal

```
SISTEMA DE GESTIÓN DE TURNOS MÉDICOS
═══════════════════════════════════════

1. Listar Pacientes
2. Listar Médicos
3. Listar Especialidades
4. Gestión de Turnos
5. Ver Turnos de un Médico
6. Ver Turnos de un Paciente
0. Salir
```

### Crear un Turno (Ejemplo)

1. Ir a **Gestión de Turnos** (opción 4)
2. Seleccionar **Crear Nuevo Turno** (opción 1)
3. Ingresar:
   - ID del Paciente: `1`
   - ID del Médico: `1`
   - ID de la Especialidad: `1`
   - Fecha y hora: `2024-12-20 10:30`
   - Duración: `30` minutos
   - Lugar: `Consultorio 1`
4. Confirmar creación

**El sistema validará automáticamente:**
- ✅ Fecha futura
- ✅ Disponibilidad del médico
- ✅ Anti-solapamiento
- ✅ Bloqueos del médico

## 📁 Estructura del Proyecto

```
sistema_turnos_medicos/
├── src/
│   ├── config/               # Configuración (Singleton)
│   │   ├── settings.py
│   │   └── __init__.py
│   ├── domain/               # Entidades (11)
│   │   ├── base.py          # BaseEntity abstracta
│   │   ├── paciente.py
│   │   ├── medico.py
│   │   ├── especialidad.py
│   │   ├── estado_turno.py
│   │   ├── turno.py
│   │   ├── disponibilidad.py
│   │   ├── consulta.py
│   │   ├── receta.py
│   │   ├── recordatorio.py
│   │   └── __init__.py
│   ├── repositories/         # Acceso a datos
│   │   ├── database.py      # DatabaseManager (Singleton)
│   │   ├── base_repository.py
│   │   ├── unit_of_work.py  # Unit of Work Pattern
│   │   ├── init_data.py     # Datos iniciales
│   │   ├── paciente_repository.py
│   │   ├── medico_repository.py
│   │   ├── especialidad_repository.py
│   │   ├── turno_repository.py
│   │   ├── estado_turno_repository.py
│   │   ├── consulta_repository.py
│   │   ├── receta_repository.py
│   │   ├── disponibilidad_repository.py
│   │   ├── recordatorio_repository.py
│   │   └── __init__.py
│   ├── services/             # Lógica de negocio
│   │   ├── turno_service.py # Servicio principal
│   │   └── __init__.py
│   ├── ui/                   # Interfaz de usuario
│   │   ├── ui_utils.py      # Utilidades Rich
│   │   ├── main_menu.py     # Menú principal
│   │   └── __init__.py
│   └── utils/                # Utilidades generales
│       ├── exceptions.py    # Excepciones personalizadas
│       └── __init__.py
├── data/                     # Base de datos (generada)
│   └── turnos_medicos.db
├── main.py                   # Punto de entrada
├── requirements.txt          # Dependencias
├── README.md                 # Este archivo
├── ARQUITECTURA.md           # Documentación técnica
└── GUIA_IMPLEMENTACION.md    # Guía de desarrollo
```

## 📚 Tecnologías Utilizadas

- **Python 3.10+**: Lenguaje principal
- **SQLAlchemy 2.0**: ORM para persistencia
- **SQLite**: Base de datos relacional
- **Rich 13.7**: Interfaz de consola profesional
- **Pydantic 2.5**: Validación de datos
- **email-validator**: Validación de emails
- **python-dateutil**: Manejo de fechas

## 🧪 Principios SOLID Aplicados

1. **S - Single Responsibility**: Cada clase tiene una única responsabilidad clara
2. **O - Open/Closed**: Extensible mediante herencia (BaseRepository, BaseEntity)
3. **L - Liskov Substitution**: Los repositorios derivados son intercambiables
4. **I - Interface Segregation**: Interfaces específicas en servicios
5. **D - Dependency Inversion**: Servicios dependen de abstracciones (repositories)

## 📝 Documentación Adicional

- **ARQUITECTURA.md**: Documentación técnica completa
- **GUIA_IMPLEMENTACION.md**: Guía para extender el sistema
- Docstrings completos en cada módulo
- Type hints en todas las funciones

## 👥 Autores

**Grupo 42**
- Oliva
- Abadía
- Giménez

**Materia**: Diseño y Arquitectura Orientada a Objetos  
**Institución**: Universidad Nacional de Cuyo - Facultad de Ingeniería  
**Año**: 2025

## 📄 Licencia

Este proyecto es de uso académico para la Universidad Nacional de Cuyo.

---

**¡Gracias por revisar nuestro proyecto!** 🎉
