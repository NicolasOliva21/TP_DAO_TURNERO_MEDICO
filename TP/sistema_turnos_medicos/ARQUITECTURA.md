# ARQUITECTURA DEL SISTEMA DE TURNOS MÉDICOS

## PATRONES DE DISEÑO IMPLEMENTADOS

### 1. Repository Pattern
- **Ubicación**: `src/repositories/`
- **Propósito**: Abstrae el acceso a datos
- **Implementación**:
  - `BaseRepository`: Clase abstracta con operaciones CRUD genéricas
  - Repositorios específicos: `PacienteRepository`, `MedicoRepository`, `TurnoRepository`, etc.

### 2. Unit of Work Pattern
- **Ubicación**: `src/repositories/unit_of_work.py`
- **Propósito**: Gestiona transacciones y coordina repositorios
- **Uso**: Context manager para garantizar consistencia transaccional

### 3. Singleton Pattern
- **Ubicación**: `src/config/settings.py`, `src/repositories/database.py`
- **Propósito**: Una única instancia de configuración y conexión DB
- **Implementación**: Uso de `__new__` para control de instanciación

### 4. Factory Pattern
- **Ubicación**: `src/services/turno_service.py`
- **Propósito**: Creación de turnos y validaciones complejas
- **Uso**: Métodos factory para crear turnos con todas las validaciones

### 5. Strategy Pattern
- **Ubicación**: `src/services/validaciones/`
- **Propósito**: Diferentes estrategias de validación
- **Implementación**: Validadores intercambiables para turnos, disponibilidad, etc.

### 6. Observer Pattern (Opcional - Recordatorios)
- **Ubicación**: `src/services/recordatorio_service.py`
- **Propósito**: Sistema de notificaciones
- **Implementación**: Observadores que reaccionan a eventos de turnos

## ARQUITECTURA EN 3 CAPAS

### Capa 1: Presentación (UI)
```
src/ui/
├── main_menu.py              # Menú principal
├── paciente_menu.py          # Gestión de pacientes
├── medico_menu.py            # Gestión de médicos
├── especialidad_menu.py      # Gestión de especialidades
├── turno_menu.py             # Gestión de turnos
├── consulta_menu.py          # Historia clínica
├── receta_menu.py            # Recetas médicas
├── reporte_menu.py           # Reportes y estadísticas
└── ui_utils.py               # Utilidades de UI
```

### Capa 2: Lógica de Negocio (Services)
```
src/services/
├── paciente_service.py       # Lógica de pacientes
├── medico_service.py         # Lógica de médicos
├── especialidad_service.py   # Lógica de especialidades
├── turno_service.py          # Lógica de turnos (anti-solape)
├── consulta_service.py       # Historia clínica
├── receta_service.py         # Recetas médicas
├── recordatorio_service.py   # Notificaciones
├── reporte_service.py        # Reportes y estadísticas
└── validaciones/             # Estrategias de validación
    ├── turno_validator.py
    ├── disponibilidad_validator.py
    └── paciente_validator.py
```

### Capa 3: Acceso a Datos (Repositories)
```
src/repositories/
├── database.py               # Gestión de conexión (Singleton)
├── base_repository.py        # Repository base (Template Method)
├── unit_of_work.py           # Unit of Work Pattern
├── paciente_repository.py
├── medico_repository.py
├── especialidad_repository.py
├── turno_repository.py
├── consulta_repository.py
├── receta_repository.py
├── estado_turno_repository.py
├── disponibilidad_repository.py
└── init_data.py              # Datos iniciales
```

## MODELO DE DOMINIO (Domain Model)

```
src/domain/
├── base.py                   # Entidad base abstracta
├── paciente.py               # Entidad Paciente
├── medico.py                 # Entidad Médico + tabla asociativa
├── especialidad.py           # Entidad Especialidad
├── estado_turno.py           # Entidad EstadoTurno
├── turno.py                  # Entidad Turno
├── disponibilidad.py         # DisponibilidadMedico, BloqueoMedico
├── consulta.py               # Entidad Consulta (historia clínica)
├── receta.py                 # Receta + ItemReceta
└── recordatorio.py           # Recordatorio
```

## VALIDACIONES IMPLEMENTADAS

### Validaciones de Pacientes
1. ✅ DNI único en base de datos
2. ✅ Email único y formato válido (regex + email-validator)
3. ✅ Fecha de nacimiento no futura
4. ✅ Campos obligatorios no vacíos
5. ✅ No permitir baja si tiene turnos futuros activos
6. ✅ Registro de usuario y fecha de modificación

### Validaciones de Médicos
1. ✅ Matrícula única e inmutable
2. ✅ DNI y email únicos
3. ✅ Horarios válidos (hora_desde < hora_hasta)
4. ✅ Al menos una especialidad asociada
5. ✅ No permitir baja si tiene turnos pendientes
6. ✅ Validación de superposición de horarios de disponibilidad
7. ✅ Registro de usuario y fecha de modificación

### Validaciones de Especialidades
1. ✅ Nombre único
2. ✅ No permitir nombre vacío
3. ✅ No permitir baja si hay médicos o turnos asociados

### Validaciones de Turnos (CRÍTICO)
1. ✅ Fecha futura obligatoria
2. ✅ Verificación de disponibilidad del médico (día y horario)
3. ✅ Anti-solape para el mismo médico
4. ✅ Anti-solape para el mismo paciente
5. ✅ Validación de especialidad del médico
6. ✅ Control de bloqueos del médico
7. ✅ Estado inicial: PEND (Pendiente)
8. ✅ Solo modificar/cancelar turnos pendientes o confirmados
9. ✅ Solo cancelar turnos futuros
10. ✅ Control de estados finales (ASIS, INAS)

### Validaciones de Consultas
1. ✅ Solo crear consulta para turnos en estado ASIS (Asistido)
2. ✅ Una consulta por turno (unique constraint)
3. ✅ Fecha de atención obligatoria

### Validaciones de Recetas
1. ✅ Solo para consultas de turnos atendidos
2. ✅ Estado inicial: ACTIVA
3. ✅ Firma digital del médico (hash)
4. ✅ Al menos un medicamento en la receta

### Validaciones de Recordatorios
1. ✅ Email válido del paciente
2. ✅ Turno en estado Reservado (PEND o CONF)
3. ✅ Envío con al menos 24h de anticipación
4. ✅ No duplicar recordatorios

## FLUJO DE UN TURNO

```
1. CREACIÓN
   - Usuario selecciona paciente, médico, especialidad, fecha/hora
   - Sistema valida disponibilidad
   - Sistema verifica anti-solape
   - Estado inicial: PEND

2. CONFIRMACIÓN (Opcional)
   - Cambio de estado PEND → CONF
   - Se puede generar recordatorio automático

3. ATENCIÓN
   - El día del turno, cambio a ASIS
   - Se crea Consulta asociada
   - Se pueden agregar Recetas

4. ESTADOS FINALES
   - ASIS: Turno atendido
   - INAS: Paciente no asistió
   - CANC: Turno cancelado
```

## ANTI-SOLAPAMIENTO DE TURNOS

### Estrategia Implementada
1. **Cálculo de intervalos**: 
   - Inicio turno: `fecha_hora`
   - Fin turno: `fecha_hora + duracion_minutos`

2. **Consulta a BD**:
   ```sql
   SELECT * FROM turnos 
   WHERE id_medico = ? 
     AND fecha_hora < turno_fin_nuevo 
     AND fecha_hora + duracion >= turno_inicio_nuevo
     AND estado IN ('PEND', 'CONF', 'ASIS')
     AND activo = TRUE
   ```

3. **Validación en servicio**:
   - Verificar disponibilidad horaria del médico
   - Verificar bloqueos del médico
   - Verificar turnos existentes del médico
   - Verificar turnos existentes del paciente

### Índices de Optimización
```sql
CREATE INDEX idx_turno_medico_fecha ON turnos(id_medico, fecha_hora);
CREATE INDEX idx_turno_paciente_fecha ON turnos(id_paciente, fecha_hora);
CREATE INDEX idx_turno_estado ON turnos(id_estado);
```

## REPORTES Y ESTADÍSTICAS

### 1. Listado de Turnos por Médico
- Entrada: id_médico, fecha_desde, fecha_hasta
- Salida: Lista de turnos con paciente, especialidad, estado

### 2. Cantidad de Turnos por Especialidad
- Entrada: fecha_desde, fecha_hasta
- Salida: Agrupación por especialidad con conteo

### 3. Pacientes Atendidos
- Entrada: fecha_desde, fecha_hasta, [médico_id], [especialidad_id]
- Salida: Lista de pacientes con turnos ASIS

### 4. Gráfico Asistencias vs Inasistencias
- Entrada: fecha_desde, fecha_hasta
- Salida: 
  - Asistencias: turnos con estado ASIS
  - Inasistencias: turnos con estado INAS o CANC sin aviso

## TECNOLOGÍAS Y HERRAMIENTAS

- **Python 3.10+**: Lenguaje base
- **SQLAlchemy 2.0**: ORM con Mapped types
- **SQLite**: Base de datos (migrable a PostgreSQL/MySQL)
- **Pydantic**: Validación de datos y DTOs
- **Rich**: UI profesional en consola
- **email-validator**: Validación de emails
- **python-dateutil**: Manejo avanzado de fechas

## PRINCIPIOS SOLID APLICADOS

1. **S - Single Responsibility**: Cada clase tiene una única responsabilidad
2. **O - Open/Closed**: Extensible mediante herencia (BaseRepository, BaseEntity)
3. **L - Liskov Substitution**: Los repositorios derivados son sustituibles
4. **I - Interface Segregation**: Interfaces específicas en servicios
5. **D - Dependency Inversion**: Servicios dependen de abstracciones (repositories)

## ESTRUCTURA DE DIRECTORIOS COMPLETA

```
sistema_turnos_medicos/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── paciente.py
│   │   ├── medico.py
│   │   ├── especialidad.py
│   │   ├── estado_turno.py
│   │   ├── turno.py
│   │   ├── disponibilidad.py
│   │   ├── consulta.py
│   │   ├── receta.py
│   │   └── recordatorio.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── base_repository.py
│   │   ├── unit_of_work.py
│   │   ├── init_data.py
│   │   ├── paciente_repository.py
│   │   ├── medico_repository.py
│   │   ├── especialidad_repository.py
│   │   ├── turno_repository.py
│   │   ├── consulta_repository.py
│   │   ├── receta_repository.py
│   │   ├── estado_turno_repository.py
│   │   └── disponibilidad_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── paciente_service.py
│   │   ├── medico_service.py
│   │   ├── especialidad_service.py
│   │   ├── turno_service.py
│   │   ├── consulta_service.py
│   │   ├── receta_service.py
│   │   ├── recordatorio_service.py
│   │   └── reporte_service.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── ui_utils.py
│   │   ├── main_menu.py
│   │   ├── paciente_menu.py
│   │   ├── medico_menu.py
│   │   ├── especialidad_menu.py
│   │   ├── turno_menu.py
│   │   ├── consulta_menu.py
│   │   ├── receta_menu.py
│   │   └── reporte_menu.py
│   └── utils/
│       ├── __init__.py
│       └── exceptions.py
├── tests/
│   ├── __init__.py
│   ├── test_paciente_service.py
│   ├── test_medico_service.py
│   ├── test_turno_service.py
│   └── test_validaciones.py
├── data/
│   └── turnos_medicos.db (generado)
├── main.py
├── requirements.txt
├── README.md
└── ARQUITECTURA.md (este archivo)
```

## EJECUCIÓN DEL PROYECTO

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar
python main.py
```

## DATOS DE EJEMPLO INICIALES

El sistema crea automáticamente:
- **Estados de Turno**: PEND, CONF, CANC, ASIS, INAS
- **Especialidades de ejemplo**: Cardiología, Pediatría, Traumatología
- **Médicos de ejemplo**: 2-3 médicos con especialidades
- **Pacientes de ejemplo**: 3-5 pacientes

## EXTENSIBILIDAD

El sistema está preparado para agregar:
- [ ] Autenticación y roles de usuario
- [ ] Envío real de emails (SMTP)
- [ ] API REST (FastAPI)
- [ ] Frontend web (React/Vue)
- [ ] Exportación de reportes a PDF/Excel
- [ ] Dashboard con gráficos interactivos
- [ ] Integración con obras sociales
- [ ] Firma digital de recetas con certificados
- [ ] Telemedicina (videollamadas)

---

**Autores**: Grupo 42 - Oliva, Abadía, Giménez  
**Materia**: Diseño y Arquitectura Orientada a Objetos  
**Fecha**: Noviembre 2025
