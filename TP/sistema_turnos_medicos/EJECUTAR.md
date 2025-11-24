# 🚀 GUÍA RÁPIDA DE EJECUCIÓN

## Paso a Paso para Ejecutar el Proyecto

### 1. Abrir PowerShell en el Directorio del Proyecto

```powershell
cd "C:\Users\nicoo\OneDrive\Documentos\Facultad\DAO\TP\sistema_turnos_medicos"
```

### 2. Crear Entorno Virtual (Primera vez)

```powershell
python -m venv venv
```

### 3. Activar Entorno Virtual

```powershell
.\venv\Scripts\Activate.ps1
```

**NOTA**: Si da error de permisos:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Instalar Dependencias (Primera vez)

```powershell
pip install -r requirements.txt
```

### 5. Ejecutar el Sistema

```powershell
python main.py
```

## ✅ Primera Ejecución - Qué Esperar

Al ejecutar por primera vez, verás:

```
============================================================
INICIALIZACIÓN DE BASE DE DATOS
============================================================

[DB] Base de datos inicializada: sqlite:///data/turnos_medicos.db
[DB] Tablas creadas exitosamente

============================================================
INICIALIZACIÓN DE DATOS BASE
============================================================

[1/4] Inicializando estados de turno...
[INIT] Estado creado: PEND - Pendiente
[INIT] Estado creado: CONF - Confirmado
[INIT] Estado creado: CANC - Cancelado
[INIT] Estado creado: ASIS - Asistido
[INIT] Estado creado: INAS - Inasistido

[2/4] Inicializando especialidades de ejemplo...
[INIT] Especialidad creada: Cardiología
[INIT] Especialidad creada: Pediatría
[INIT] Especialidad creada: Traumatología
[INIT] Especialidad creada: Dermatología
[INIT] Especialidad creada: Oftalmología

[3/4] Inicializando médicos de ejemplo...
[INIT] Médico creado: Dra. María González - MP12345
[INIT] Médico creado: Dr. Juan Pérez - MP54321
[INIT] Médico creado: Dra. Ana Martínez - MP98765

[4/4] Inicializando pacientes de ejemplo...
[INIT] Paciente creado: Carlos Rodríguez - DNI 35123456
[INIT] Paciente creado: Laura Fernández - DNI 40987654
[INIT] Paciente creado: Roberto Gómez - DNI 38456789
[INIT] Paciente creado: Sofía López - DNI 42789123

============================================================
INICIALIZACIÓN COMPLETADA EXITOSAMENTE
============================================================

[Aparece el menú principal]
```

## 📋 Datos de Ejemplo Cargados

### Pacientes (4)
| ID | DNI      | Nombre           | Email                        |
|----|----------|------------------|------------------------------|
| 1  | 35123456 | Carlos Rodríguez | carlos.rodriguez@email.com   |
| 2  | 40987654 | Laura Fernández  | laura.fernandez@email.com    |
| 3  | 38456789 | Roberto Gómez    | roberto.gomez@email.com      |
| 4  | 42789123 | Sofía López      | sofia.lopez@email.com        |

### Médicos (3)
| ID | Matrícula | Nombre          | Especialidades            |
|----|-----------|-----------------|---------------------------|
| 1  | MP12345   | María González  | Cardiología               |
| 2  | MP54321   | Juan Pérez      | Pediatría, Traumatología  |
| 3  | MP98765   | Ana Martínez    | Traumatología             |

### Especialidades (5)
| ID | Nombre         |
|----|----------------|
| 1  | Cardiología    |
| 2  | Pediatría      |
| 3  | Traumatología  |
| 4  | Dermatología   |
| 5  | Oftalmología   |

### Horarios de Atención

**Dra. María González (Cardiología)**
- Lunes: 08:00 - 12:00
- Miércoles: 08:00 - 12:00
- Viernes: 08:00 - 12:00

**Dr. Juan Pérez (Pediatría, Traumatología)**
- Martes: 14:00 - 18:00
- Jueves: 14:00 - 18:00

**Dra. Ana Martínez (Traumatología)**
- Lunes a Viernes: 09:00 - 13:00

## 🎯 Ejemplo: Crear un Turno

### Opción 4 → Gestión de Turnos → Opción 1 (Crear Nuevo Turno)

```
ID del Paciente: 1
ID del Médico: 1
ID de la Especialidad: 1
Fecha y hora del turno (AAAA-MM-DD HH:MM): 2024-12-23 10:00
Duración en minutos [30]: 30
Lugar del turno [Consultorio]: Consultorio 1
Observaciones: 

¿Confirma la creación del turno? [s/N]: s

✓ Turno creado exitosamente (ID: 1)
ℹ Estado: Pendiente
```

## ⚠️ Validaciones que Verás

### Fecha Pasada
```
ID del Paciente: 1
ID del Médico: 1
Fecha y hora: 2024-01-01 10:00

✗ Error: La fecha del turno debe ser futura
```

### Médico Sin Disponibilidad
```
ID del Médico: 1
Fecha y hora: 2024-12-23 15:00  ← Dra. González no atiende a la tarde

✗ Error: El médico no atiende en ese horario los días Lunes
```

### Turno Solapado
```
[Si ya existe un turno el 2024-12-23 10:00 para el médico]

✗ Error: El médico ya tiene un turno asignado en ese horario
```

### Especialidad No Corresponde
```
ID del Médico: 1  (Cardiología)
ID de la Especialidad: 2  (Pediatría)

✗ Error: El médico María González no tiene la especialidad Pediatría
```

## 📱 Navegación del Menú

### Menú Principal
```
1. Listar Pacientes          ← Ver todos los pacientes
2. Listar Médicos            ← Ver médicos con especialidades
3. Listar Especialidades     ← Ver especialidades disponibles
4. Gestión de Turnos         ← SUBMENU de turnos
5. Ver Turnos de un Médico   ← Historial por médico
6. Ver Turnos de un Paciente ← Historial por paciente
0. Salir                     ← Cerrar sistema
```

### Gestión de Turnos (Opción 4)
```
1. Crear Nuevo Turno         ← Crear con validaciones
2. Cancelar Turno            ← Cambiar a estado CANCELADO
3. Confirmar Turno           ← PEND → CONF
4. Marcar como Asistido      ← PEND/CONF → ASIS
5. Marcar como Inasistido    ← PEND/CONF → INAS
0. Volver
```

## 🐛 Solución de Problemas

### Error: "python" no se reconoce
**Solución**: Instala Python desde python.org o usa `py` en lugar de `python`:
```powershell
py main.py
```

### Error: Cannot import name 'X'
**Solución**: Reinstala dependencias:
```powershell
pip install -r requirements.txt --force-reinstall
```

### Error: Database is locked
**Solución**: Cierra todos los procesos de Python y vuelve a ejecutar:
```powershell
python main.py
```

### Base de datos corrupta
**Solución**: Elimina la BD y vuelve a ejecutar:
```powershell
Remove-Item -Path "data\turnos_medicos.db" -Force
python main.py
```

## 📊 Estados de Turno

| Código | Nombre      | Descripción                              |
|--------|-------------|------------------------------------------|
| PEND   | Pendiente   | Turno reservado, sin confirmar           |
| CONF   | Confirmado  | Paciente confirmó asistencia             |
| CANC   | Cancelado   | Turno cancelado antes de la fecha        |
| ASIS   | Asistido    | Paciente concurrió a la consulta         |
| INAS   | Inasistido  | Paciente no asistió                      |

### Transiciones Válidas
```
PEND → CONF → ASIS
  ↓      ↓      
CANC   INAS
```

## 🔄 Ejecuciones Posteriores

A partir de la segunda ejecución:
- ✅ Los datos persisten en la base de datos
- ✅ No se duplican datos de ejemplo
- ✅ Puedes seguir trabajando con los turnos creados

## 💡 Tips

1. **Ver IDs**: Usa opciones 1, 2 y 3 para ver IDs antes de crear turnos
2. **Formato de fecha**: Siempre `AAAA-MM-DD HH:MM` (ej: 2024-12-25 10:30)
3. **Horarios**: Respeta los horarios de disponibilidad de cada médico
4. **Cancelar turno**: Usa opción 4→2 con el ID del turno

## 📚 Archivos Importantes

- `README_NUEVO.md`: Documentación completa
- `ARQUITECTURA.md`: Detalles técnicos de arquitectura
- `GUIA_IMPLEMENTACION.md`: Cómo extender el sistema
- `main.py`: Punto de entrada
- `data/turnos_medicos.db`: Base de datos SQLite (generada)

---

**¿Necesitas ayuda?** Revisa `README_NUEVO.md` para documentación completa.

**¡Listo para ejecutar!** 🚀
```powershell
python main.py
```
