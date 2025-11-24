# ✅ CHECKLIST DE TESTING

## Pre-ejecución

```powershell
# 1. Verificar que estás en el directorio correcto
cd "C:\Users\nicoo\OneDrive\Documentos\Facultad\DAO\TP\sistema_turnos_medicos"

# 2. Activar entorno virtual (si ya lo creaste)
.\venv\Scripts\Activate.ps1

# 3. Si NO has creado el entorno, créalo primero:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Test 1: Ejecución Inicial ✅

**Comando**: `python main.py`

**Esperas ver**:
```
============================================================
INICIALIZACIÓN DE BASE DE DATOS
============================================================
[DB] Base de datos inicializada: sqlite:///data/turnos_medicos.db
[DB] Tablas creadas exitosamente
...
[INIT] Estado creado: PEND - Pendiente
...
[INIT] Especialidad creada: Cardiología
...
[INIT] Médico creado: Dra. María González - MP12345
...
[INIT] Paciente creado: Carlos Rodríguez - DNI 35123456
...
INICIALIZACIÓN COMPLETADA EXITOSAMENTE
```

**✅ Pasar**: Si ves el menú principal sin errores  
**❌ Fallar**: Si hay errores de importación

---

## Test 2: Listar Datos ✅

### 2.1 Listar Pacientes

**Pasos**: Opción 1

**Esperas ver**:
```
┌────┬──────────┬──────────────────┬────────────────────────┬──────────┬──────────────┐
│ ID │ DNI      │ Nombre Completo  │ Email                  │ Teléfono │ Obra Social  │
├────┼──────────┼──────────────────┼────────────────────────┼──────────┼──────────────┤
│ 1  │ 35123456 │ Carlos Rodríguez │ carlos.rodriguez@em... │ 261-...  │ OSDE         │
└────┴──────────┴──────────────────┴────────────────────────┴──────────┴──────────────┘
ℹ Total: 4 paciente(s)
```

**✅ Pasar**: Si ves tabla con 4 pacientes  
**❌ Fallar**: Si no hay pacientes o hay error

### 2.2 Listar Médicos

**Pasos**: Opción 2

**Esperas ver**:
```
┌────┬───────────┬─────────────────┬──────────────────────────┬───────────────────────┐
│ ID │ Matrícula │ Nombre Completo │ Especialidades           │ Email                 │
├────┼───────────┼─────────────────┼──────────────────────────┼───────────────────────┤
│ 1  │ MP12345   │ María González  │ Cardiología              │ maria.gonzalez@...    │
│ 2  │ MP54321   │ Juan Pérez      │ Pediatría, Traumatología │ juan.perez@...        │
└────┴───────────┴─────────────────┴──────────────────────────┴───────────────────────┘
ℹ Total: 3 médico(s)
```

**✅ Pasar**: Si ves tabla con 3 médicos  
**❌ Fallar**: Si no hay médicos o hay error

### 2.3 Listar Especialidades

**Pasos**: Opción 3

**Esperas ver**:
```
┌────┬───────────────┬──────────────────────────────────┐
│ ID │ Nombre        │ Descripción                      │
├────┼───────────────┼──────────────────────────────────┤
│ 1  │ Cardiología   │ Especialidad médica que se...    │
└────┴───────────────┴──────────────────────────────────┘
ℹ Total: 5 especialidad(es)
```

**✅ Pasar**: Si ves tabla con 5 especialidades  
**❌ Fallar**: Si no hay especialidades o hay error

---

## Test 3: Crear Turno Exitoso ✅

**Pasos**: 
1. Opción 4 (Gestión de Turnos)
2. Opción 1 (Crear Nuevo Turno)

**Datos a ingresar**:
```
ID del Paciente: 1
ID del Médico: 1
ID de la Especialidad: 1
Fecha y hora: 2024-12-23 10:00  ← Asegúrate que sea LUNES y FUTURO
Duración: 30
Lugar: Consultorio 1
Observaciones: [Enter - vacío]
¿Confirma? s
```

**Esperas ver**:
```
✓ Turno creado exitosamente (ID: 1)
ℹ Estado: Pendiente
```

**✅ Pasar**: Si el turno se crea sin errores  
**❌ Fallar**: Si hay error de validación

---

## Test 4: Validación de Fecha Pasada ❌ (Debe Fallar)

**Pasos**:
1. Opción 4 → 1 (Crear Turno)

**Datos a ingresar**:
```
ID del Paciente: 2
ID del Médico: 1
ID de la Especialidad: 1
Fecha y hora: 2024-01-01 10:00  ← Fecha PASADA
```

**Esperas ver**:
```
✗ Error: La fecha del turno debe ser futura
```

**✅ Pasar**: Si muestra el error y NO crea el turno  
**❌ Fallar**: Si crea el turno con fecha pasada

---

## Test 5: Validación de Disponibilidad ❌ (Debe Fallar)

**Pasos**:
1. Opción 4 → 1 (Crear Turno)

**Datos a ingresar**:
```
ID del Paciente: 2
ID del Médico: 1  ← Dra. González atiende Lu/Mi/Vi 8-12
ID de la Especialidad: 1
Fecha y hora: 2024-12-23 15:00  ← Lunes a las 15:00 (fuera de horario)
```

**Esperas ver**:
```
✗ Error: El médico no atiende en ese horario los días Lunes
```

**✅ Pasar**: Si muestra el error de disponibilidad  
**❌ Fallar**: Si permite crear el turno fuera de horario

---

## Test 6: Validación de Solapamiento ❌ (Debe Fallar)

**Pre-requisito**: Debes haber creado el turno del Test 3

**Pasos**:
1. Opción 4 → 1 (Crear Turno)

**Datos a ingresar**:
```
ID del Paciente: 2  ← Paciente diferente
ID del Médico: 1    ← Mismo médico
ID de la Especialidad: 1
Fecha y hora: 2024-12-23 10:00  ← Misma fecha/hora que Test 3
```

**Esperas ver**:
```
✗ Error: El médico ya tiene un turno asignado en ese horario
```

**✅ Pasar**: Si detecta el solapamiento y NO crea el turno  
**❌ Fallar**: Si permite dos turnos al mismo médico a la misma hora

---

## Test 7: Validación de Especialidad ❌ (Debe Fallar)

**Pasos**:
1. Opción 4 → 1 (Crear Turno)

**Datos a ingresar**:
```
ID del Paciente: 3
ID del Médico: 1  ← Dra. González: Cardiología
ID de la Especialidad: 2  ← Pediatría (no la tiene)
Fecha y hora: 2024-12-25 10:00  ← Miércoles futuro
```

**Esperas ver**:
```
✗ Error: El médico María González no tiene la especialidad Pediatría
```

**✅ Pasar**: Si valida la especialidad del médico  
**❌ Fallar**: Si permite asignar especialidad incorrecta

---

## Test 8: Cambio de Estado de Turno ✅

**Pre-requisito**: Debes tener el turno ID 1 del Test 3

### 8.1 Confirmar Turno

**Pasos**:
1. Opción 4 (Gestión de Turnos)
2. Opción 3 (Confirmar Turno)
3. ID: `1`

**Esperas ver**:
```
✓ Turno #1 confirmado exitosamente
```

### 8.2 Marcar Asistido

**Pasos**:
1. Opción 4
2. Opción 4 (Marcar Asistido)
3. ID: `1`

**Esperas ver**:
```
✓ Turno #1 marcado como ASISTIDO
```

**✅ Pasar**: Si los cambios de estado funcionan  
**❌ Fallar**: Si hay error al cambiar estados

---

## Test 9: Ver Turnos del Médico ✅

**Pasos**:
1. Opción 5 (Ver Turnos de un Médico)
2. ID: `1`

**Esperas ver**:
```
┌────┬──────────────────┬─────────────────┬──────────┬──────────┬──────────────┐
│ ID │ Paciente         │ Fecha/Hora      │ Duración │ Estado   │ Lugar        │
├────┼──────────────────┼─────────────────┼──────────┼──────────┼──────────────┤
│ 1  │ Carlos Rodríguez │ 23/12/2024 10:00│ 30 min   │ Asistido │ Consultorio 1│
└────┴──────────────────┴─────────────────┴──────────┴──────────┴──────────────┘
ℹ Total: 1 turno(s)
```

**✅ Pasar**: Si muestra el turno creado  
**❌ Fallar**: Si no muestra turnos o hay error

---

## Test 10: Persistencia ✅

**Pasos**:
1. Salir del sistema (Opción 0)
2. Volver a ejecutar: `python main.py`
3. Opción 5, ID: `1`

**Esperas ver**:
- El turno creado anteriormente SIGUE EXISTIENDO

**✅ Pasar**: Si los datos persisten  
**❌ Fallar**: Si los turnos desaparecen

---

## ✅ RESUMEN DE TESTS

| # | Test | Resultado Esperado | Aprobado |
|---|------|-------------------|----------|
| 1 | Ejecución inicial | Menú sin errores | ☐ |
| 2.1 | Listar Pacientes | 4 pacientes | ☐ |
| 2.2 | Listar Médicos | 3 médicos | ☐ |
| 2.3 | Listar Especialidades | 5 especialidades | ☐ |
| 3 | Crear turno OK | Turno creado | ☐ |
| 4 | Validar fecha pasada | Error mostrado | ☐ |
| 5 | Validar disponibilidad | Error mostrado | ☐ |
| 6 | Validar solapamiento | Error mostrado | ☐ |
| 7 | Validar especialidad | Error mostrado | ☐ |
| 8 | Cambiar estado | Estados cambiados | ☐ |
| 9 | Ver turnos médico | Turno visible | ☐ |
| 10 | Persistencia | Datos persisten | ☐ |

---

## 🐛 Si Algo Falla

### ImportError
```powershell
pip install -r requirements.txt --force-reinstall
```

### SQLAlchemy not found
```powershell
pip install sqlalchemy rich pydantic email-validator python-dateutil
```

### Database locked
```powershell
# Cerrar todo y volver a ejecutar
python main.py
```

### Limpiar y empezar de cero
```powershell
Remove-Item -Path "data\turnos_medicos.db" -Force
python main.py
```

---

## 📊 Criterios de Aprobación

✅ **Aprobado** si:
- 10/10 tests pasan
- No hay errores de importación
- Las validaciones funcionan correctamente
- Los datos persisten

⚠️ **Revisar** si:
- 7-9 tests pasan
- Hay algunos warnings

❌ **No Aprobado** si:
- < 7 tests pasan
- Hay errores críticos

---

## 🎯 Tests Críticos (Mínimos)

Estos 5 tests SON OBLIGATORIOS:

1. ✅ Test 1: Sistema ejecuta sin errores
2. ✅ Test 3: Crear turno exitoso
3. ✅ Test 6: Validación anti-solapamiento
4. ✅ Test 9: Ver turnos del médico
5. ✅ Test 10: Persistencia de datos

**Si estos 5 pasan, el proyecto es FUNCIONAL** ✅

---

**¡Listo para probar!** 🚀

```powershell
python main.py
```
