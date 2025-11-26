/**
 * Aplicación Principal - Sistema de Turnos Médicos
 * Maneja la lógica de la interfaz y la interacción con la API
 */

// ============================================================
// ESTADO GLOBAL DE LA APLICACIÓN
// ============================================================

const appState = {
    pacienteSeleccionado: null,
    especialidadSeleccionada: null,
    medicoSeleccionado: null,
    horarioSeleccionado: null,
    currentStep: 1,
};

// ============================================================
// NAVEGACIÓN
// ============================================================

function navigateTo(page) {
    // Desactivar todos los botones de navegación
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Activar el botón actual
    const activeBtn = document.querySelector(`[data-page="${page}"]`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }

    // Ocultar todas las páginas
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });

    // Mostrar la página seleccionada
    const activePage = document.getElementById(`${page}-page`);
    if (activePage) {
        activePage.classList.add('active');
    }

    // Cargar datos según la página
    switch (page) {
        case 'home':
            loadHomeStats();
            break;
        case 'turnos':
            resetReservaTurno();
            break;
        case 'pacientes':
            loadPacientesTable();
            break;
        case 'medicos':
            loadMedicosTable();
            loadEspecialidadesCheckboxes();
            break;
        case 'reportes':
            actualizarReportes();
            break;
    }
}

// Event listeners para navegación
document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const page = btn.getAttribute('data-page');
        navigateTo(page);
    });
});

// ============================================================
// UTILIDADES UI
// ============================================================

function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;

    const icon = type === 'success' ? 'fa-check-circle' :
        type === 'error' ? 'fa-exclamation-circle' :
            'fa-info-circle';

    toast.innerHTML = `
        <i class="fas ${icon}"></i>
        <span class="toast-message">${message}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-AR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    });
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('es-AR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('es-AR', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// ============================================================
// HOME PAGE - ESTADÍSTICAS
// ============================================================

async function loadHomeStats() {
    try {
        showLoading();

        const [medicos, especialidades, pacientes, turnos] = await Promise.all([
            api.getMedicos(),
            api.getEspecialidades(),
            api.getPacientes(),
            api.getTurnos({ limit: 1000 })
        ]);

        document.getElementById('stat-medicos').textContent = medicos.length;
        document.getElementById('stat-especialidades').textContent = especialidades.length;
        document.getElementById('stat-pacientes').textContent = pacientes.length;

        // Contar turnos activos (no cancelados)
        const turnosActivos = turnos.filter(t =>
            t.estado.codigo !== 'CANC' && t.estado.codigo !== 'INAS'
        );
        document.getElementById('stat-turnos').textContent = turnosActivos.length;

    } catch (error) {
        console.error('Error cargando estadísticas:', error);
    } finally {
        hideLoading();
    }
}

// ============================================================
// GESTIÓN DE TABS
// ============================================================

document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        const tabId = btn.getAttribute('data-tab');
        const parent = btn.closest('.card');

        // Desactivar todos los tabs
        parent.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        parent.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

        // Activar el tab seleccionado
        btn.classList.add('active');
        parent.querySelector(`#${tabId}`).classList.add('active');
    });
});

// ============================================================
// STEPPER - NAVEGACIÓN ENTRE PASOS
// ============================================================

function updateStepper(step) {
    appState.currentStep = step;

    // Actualizar visual del stepper
    document.querySelectorAll('.step').forEach((stepEl, index) => {
        stepEl.classList.remove('active', 'completed');
        if (index + 1 < step) {
            stepEl.classList.add('completed');
        } else if (index + 1 === step) {
            stepEl.classList.add('active');
        }
    });

    // Mostrar contenido del paso
    document.querySelectorAll('.step-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`step-${step}`).classList.add('active');
}

function nextStep(step) {
    // Validar paso actual antes de avanzar
    if (!validateStep(appState.currentStep)) {
        return;
    }

    updateStepper(step);

    // Cargar datos del siguiente paso
    switch (step) {
        case 2:
            loadEspecialidades();
            break;
        case 3:
            loadMedicosPorEspecialidad();
            break;
        case 4:
            cargarHorariosDisponibles();
            break;
        case 5:
            mostrarResumenTurno();
            break;
    }
}

function prevStep(step) {
    updateStepper(step);
}

function validateStep(step) {
    switch (step) {
        case 1:
            if (!appState.pacienteSeleccionado) {
                showToast('Debe seleccionar o registrar un paciente', 'warning');
                return false;
            }
            return true;
        case 2:
            if (!appState.especialidadSeleccionada) {
                showToast('Debe seleccionar una especialidad', 'warning');
                return false;
            }
            return true;
        case 3:
            if (!appState.medicoSeleccionado) {
                showToast('Debe seleccionar un médico', 'warning');
                return false;
            }
            return true;
        case 4:
            if (!appState.horarioSeleccionado) {
                showToast('Debe seleccionar un horario', 'warning');
                return false;
            }
            return true;
        default:
            return true;
    }
}

function resetReservaTurno() {
    appState.pacienteSeleccionado = null;
    appState.especialidadSeleccionada = null;
    appState.medicoSeleccionado = null;
    appState.horarioSeleccionado = null;
    updateStepper(1);

    // Reset calendario
    calendarioState.semanaActual = 0;
    calendarioState.horariosTodos = {};
    calendarioState.turnosOcupados = [];

    // Limpiar formularios
    document.getElementById('buscar-dni').value = '';
    document.getElementById('paciente-encontrado').style.display = 'none';
    document.getElementById('form-nuevo-paciente').reset();
}

// ============================================================
// PASO 1: PACIENTE
// ============================================================

async function buscarPaciente() {
    const dni = document.getElementById('buscar-dni').value.trim();

    if (!dni) {
        showToast('Ingrese un DNI', 'warning');
        return;
    }

    try {
        showLoading();
        const paciente = await api.getPacienteByDNI(dni);

        appState.pacienteSeleccionado = paciente;

        // Mostrar información del paciente
        document.getElementById('pac-nombre').textContent =
            `${paciente.nombre} ${paciente.apellido}`;
        document.getElementById('pac-dni').textContent = paciente.dni;
        document.getElementById('pac-email').textContent = paciente.email;
        document.getElementById('pac-telefono').textContent = paciente.telefono;

        document.getElementById('paciente-encontrado').style.display = 'block';
        document.getElementById('btn-step-1').disabled = false;

        showToast('Paciente encontrado', 'success');

    } catch (error) {
        showToast('Paciente no encontrado. Puede registrar uno nuevo.', 'error');
        document.getElementById('paciente-encontrado').style.display = 'none';

        // Cambiar al tab de nuevo paciente
        document.querySelector('[data-tab="nuevo-paciente"]').click();
        document.getElementById('pac-nuevo-dni').value = dni;
    } finally {
        hideLoading();
    }
}

// Event listener para buscar con Enter
document.getElementById('buscar-dni').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        buscarPaciente();
    }
});

// Formulario de nuevo paciente
document.getElementById('form-nuevo-paciente').addEventListener('submit', async (e) => {
    e.preventDefault();

    const pacienteData = {
        dni: document.getElementById('pac-nuevo-dni').value.trim(),
        nombre: document.getElementById('pac-nombre-input').value.trim(),
        apellido: document.getElementById('pac-apellido').value.trim(),
        email: document.getElementById('pac-email-input').value.trim(),
        telefono: document.getElementById('pac-telefono-input').value.trim(),
        fecha_nacimiento: document.getElementById('pac-fecha-nacimiento').value,
        direccion: document.getElementById('pac-direccion').value.trim(),
        obra_social: document.getElementById('pac-obra-social').value.trim() || null,
        numero_afiliado: document.getElementById('pac-numero-afiliado').value.trim() || null,
    };

    try {
        showLoading();
        const paciente = await api.createPaciente(pacienteData);

        appState.pacienteSeleccionado = paciente;

        showToast('Paciente registrado exitosamente', 'success');

        // Cambiar al tab de buscar y mostrar el paciente creado
        document.querySelector('[data-tab="buscar-paciente"]').click();
        document.getElementById('buscar-dni').value = paciente.dni;
        await buscarPaciente();

    } catch (error) {
        showToast(`Error al registrar paciente: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
});

// ============================================================
// PASO 2: ESPECIALIDAD
// ============================================================

async function loadEspecialidades() {
    try {
        showLoading();
        const especialidades = await api.getEspecialidades();

        const grid = document.getElementById('especialidades-grid');
        grid.innerHTML = '';

        especialidades.forEach(esp => {
            const card = document.createElement('div');
            card.className = 'especialidad-card';
            card.innerHTML = `
                <h3>${esp.nombre}</h3>
                <p>${esp.descripcion || 'Sin descripción'}</p>
            `;

            card.addEventListener('click', () => {
                // Desmarcar todas
                document.querySelectorAll('.especialidad-card').forEach(c =>
                    c.classList.remove('selected')
                );

                // Marcar esta
                card.classList.add('selected');
                appState.especialidadSeleccionada = esp;
                document.getElementById('btn-step-2').disabled = false;
            });

            grid.appendChild(card);
        });

    } catch (error) {
        showToast('Error al cargar especialidades', 'error');
    } finally {
        hideLoading();
    }
}

// ============================================================
// PASO 3: MÉDICO
// ============================================================

async function loadMedicosPorEspecialidad() {
    try {
        showLoading();
        const medicos = await api.getMedicosByEspecialidad(
            appState.especialidadSeleccionada.id
        );

        const list = document.getElementById('medicos-list');
        list.innerHTML = '';

        if (medicos.length === 0) {
            list.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No hay médicos disponibles para esta especialidad</p>';
            return;
        }

        medicos.forEach(med => {
            const card = document.createElement('div');
            card.className = 'medico-card';

            const iniciales = `${med.nombre[0]}${med.apellido[0]}`;

            card.innerHTML = `
                <div class="medico-avatar">${iniciales}</div>
                <div class="medico-info">
                    <h3>Dr. ${med.nombre} ${med.apellido}</h3>
                    <p>Matrícula: ${med.matricula}</p>
                </div>
            `;

            card.addEventListener('click', () => {
                // Desmarcar todos
                document.querySelectorAll('.medico-card').forEach(c =>
                    c.classList.remove('selected')
                );

                // Marcar este
                card.classList.add('selected');
                appState.medicoSeleccionado = med;
                document.getElementById('btn-step-3').disabled = false;
            });

            list.appendChild(card);
        });

    } catch (error) {
        showToast('Error al cargar médicos', 'error');
    } finally {
        hideLoading();
    }
}

// ============================================================
// PASO 4: HORARIO (CALENDARIO SEMANAL)
// ============================================================

// Estado del calendario
const calendarioState = {
    semanaActual: 0, // 0 = semana actual, 1 = siguiente, etc.
    horariosTodos: {}, // Todos los horarios disponibles
    turnosOcupados: [], // Turnos ya reservados
};

async function cargarHorariosDisponibles() {
    try {
        showLoading();

        // Obtener calendario completo del médico
        const calendario = await api.getCalendarioDisponibilidad(appState.medicoSeleccionado.id, 30, 30);
        calendarioState.horariosTodos = calendario;

        console.log('Horarios disponibles cargados:', Object.keys(calendario).length, 'fechas');
        console.log('Fechas disponibles:', Object.keys(calendario));
        console.log('Muestra de horarios:', calendario);

        // Mostrar la primera fecha con horarios
        const primeraFecha = Object.keys(calendario)[0];
        if (primeraFecha) {
            console.log(`Primera fecha disponible: ${primeraFecha}`);
            console.log('Horarios para esa fecha:', calendario[primeraFecha]);
        }

        // Intentar obtener turnos ocupados del médico (opcional - para mostrar info visual)
        // Si falla, el calendario seguirá funcionando mostrando solo disponibilidad
        calendarioState.turnosOcupados = [];
        try {
            const turnosOcupados = await api.getTurnosByMedico(appState.medicoSeleccionado.id);
            if (Array.isArray(turnosOcupados)) {
                calendarioState.turnosOcupados = turnosOcupados;
                console.log(`Turnos ocupados cargados: ${turnosOcupados.length}`);
            }
        } catch (error) {
            console.warn('No se pudieron cargar turnos ocupados (esto no afecta la funcionalidad):', error.message);
            // Continuar sin turnos ocupados - el calendario solo mostrará disponibilidad
        }

        // Renderizar calendario
        renderizarCalendarioSemanal();

    } catch (error) {
        console.error('Error al cargar calendario:', error);
        showToast('Error al cargar horarios disponibles', 'error');
        document.getElementById('calendario-semanal').innerHTML =
            '<p style="text-align: center; padding: 3rem; color: var(--danger-color);">Error al cargar horarios</p>';
    } finally {
        hideLoading();
    }
}

function cambiarSemana(direccion) {
    calendarioState.semanaActual += direccion;
    if (calendarioState.semanaActual < 0) {
        calendarioState.semanaActual = 0;
        showToast('No se pueden ver semanas anteriores', 'info');
        return;
    }
    renderizarCalendarioSemanal();
}

function renderizarCalendarioSemanal() {
    console.log('=== INICIANDO RENDERIZADO DE CALENDARIO SEMANAL ===');
    const container = document.getElementById('calendario-semanal');
    if (!container) {
        console.error('ERROR: No se encontró el contenedor calendario-semanal');
        return;
    }

    // Verificar que el container tenga la clase para el grid
    if (!container.classList.contains('calendario-semanal')) {
        container.classList.add('calendario-semanal');
        console.log('Clase calendario-semanal agregada al container');
    }

    // FORZAR GRID con estilos inline como fallback
    container.style.display = 'grid';
    container.style.gridTemplateColumns = '80px repeat(7, 1fr)';
    container.style.minWidth = '800px';

    container.innerHTML = '';
    console.log('Container limpiado - Grid forzado con estilos inline');

    // Calcular fechas de la semana
    const hoy = new Date();
    hoy.setHours(0, 0, 0, 0);

    const inicioSemana = new Date(hoy);
    inicioSemana.setDate(hoy.getDate() + (calendarioState.semanaActual * 7));

    // Ajustar al lunes de la semana
    const diaSemana = inicioSemana.getDay();
    const diferencia = diaSemana === 0 ? -6 : 1 - diaSemana;
    inicioSemana.setDate(inicioSemana.getDate() + diferencia);

    const diasSemana = [];
    for (let i = 0; i < 7; i++) {
        const dia = new Date(inicioSemana);
        dia.setDate(inicioSemana.getDate() + i);
        diasSemana.push(dia);
    }

    console.log('Días de la semana calculados:', diasSemana.length);

    // Actualizar texto de semana actual
    const primerDia = diasSemana[0];
    const ultimoDia = diasSemana[6];
    const semanaTexto = document.getElementById('semana-texto');
    if (semanaTexto) {
        semanaTexto.textContent =
            `${primerDia.getDate()} ${primerDia.toLocaleDateString('es-AR', { month: 'short' })} - ${ultimoDia.getDate()} ${ultimoDia.toLocaleDateString('es-AR', { month: 'short', year: 'numeric' })}`;
    }

    // Definir horarios (de 8:00 a 19:00 - 12 slots de 1 hora)
    const horasDelDia = [];
    for (let hora = 8; hora < 20; hora++) {
        horasDelDia.push(hora.toString().padStart(2, '0'));
    }

    console.log(`Creando grid de ${horasDelDia.length} horas x 7 días`);

    // Crear encabezado - esquina
    const headerCorner = document.createElement('div');
    headerCorner.className = 'cal-header-corner';
    headerCorner.innerHTML = '<i class="fas fa-clock"></i>';
    container.appendChild(headerCorner);

    // Crear encabezados de días
    const nombresDias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'];
    diasSemana.forEach((dia, index) => {
        const headerDia = document.createElement('div');
        headerDia.className = 'cal-header-dia';

        const esHoy = dia.toDateString() === hoy.toDateString();
        if (esHoy) {
            headerDia.style.background = 'linear-gradient(135deg, #059669, #10b981)';
        }

        headerDia.innerHTML = `
            <span class="cal-dia-nombre">${nombresDias[index]}</span>
            <span class="cal-dia-numero">${dia.getDate()}</span>
        `;
        container.appendChild(headerDia);
    });

    console.log('Encabezados creados');

    // Crear filas de horarios
    let celdasCreadas = 0;
    horasDelDia.forEach(hora => {
        // Label de hora
        const horaLabel = document.createElement('div');
        horaLabel.className = 'cal-hora-label';
        horaLabel.textContent = `${hora}:00`;
        container.appendChild(horaLabel);

        // Celdas de cada día
        diasSemana.forEach((dia, indexDia) => {
            const celda = document.createElement('div');
            celda.className = 'cal-celda';

            const fechaStr = dia.toISOString().split('T')[0];

            // Debug para el primer día y primera hora
            if (celdasCreadas === 0) {
                console.log(`🔍 Primera celda - Día:`, dia, `fechaStr:`, fechaStr, `hora:`, hora);
                console.log(`Buscando en calendarioState.horariosTodos['${fechaStr}']:`, calendarioState.horariosTodos[fechaStr]);
            }

            // Buscar si hay horario disponible (hora es "08", "09", etc.)
            const horarioDisponible = buscarHorarioDisponible(fechaStr, hora);

            // Buscar si hay turno ocupado
            const turnoOcupado = buscarTurnoOcupado(fechaStr, hora);

            if (turnoOcupado) {
                // Celda ocupada - mostrar información del turno
                const colores = ['', 'amarillo', 'verde', 'rosa'];
                const colorAleatorio = colores[Math.floor(Math.random() * colores.length)];
                celda.classList.add('ocupado', colorAleatorio);

                const horaTurno = new Date(turnoOcupado.fecha_hora);
                celda.innerHTML = `
                    <div class="turno-info">
                        <div class="turno-hora">${horaTurno.toLocaleTimeString('es-AR', { hour: '2-digit', minute: '2-digit' })}</div>
                        <div class="turno-materia">Turno Reservado</div>
                        <div class="turno-aula">Paciente: ${turnoOcupado.paciente?.nombre || 'N/A'}</div>
                    </div>
                `;
            } else if (horarioDisponible) {
                // Celda disponible
                celda.classList.add('disponible');
                celda.dataset.horario = horarioDisponible;

                celda.addEventListener('click', () => {
                    // Desmarcar todas las celdas
                    document.querySelectorAll('.cal-celda').forEach(c => {
                        c.classList.remove('seleccionado');
                    });

                    // Marcar esta celda
                    celda.classList.add('seleccionado');
                    appState.horarioSeleccionado = horarioDisponible;

                    // Habilitar botón siguiente
                    document.getElementById('btn-step-4').disabled = false;

                    // Mostrar feedback
                    const fecha = new Date(horarioDisponible);
                    showToast(`Horario seleccionado: ${fecha.toLocaleString('es-AR')}`, 'success');
                });
            } else {
                // Celda sin disponibilidad (día que el médico no trabaja)
                celda.classList.add('no-disponible');
                celda.style.background = '#f8f9fa';
                celda.style.cursor = 'not-allowed';
                celda.style.border = '1px solid #e2e8f0';
            }

            container.appendChild(celda);
            celdasCreadas++;
        });
    });

    console.log(`=== CALENDARIO COMPLETADO: ${celdasCreadas} celdas creadas ===`);
}

function buscarHorarioDisponible(fecha, hora) {
    // Buscar en los horarios disponibles
    if (!calendarioState.horariosTodos[fecha]) {
        return null;
    }

    const horarios = calendarioState.horariosTodos[fecha];

    // Buscar cualquier horario que comience con la hora especificada
    // Los timestamps vienen como "2025-11-24T08:00:00", "2025-11-24T08:30:00", etc.
    const horarioEncontrado = horarios.find(h => {
        // Extraer la hora del timestamp directamente del string
        // Formato: "2025-11-24T08:00:00" -> extraer "08"
        const horaStr = h.substring(11, 13); // Posiciones 11-12 son la hora
        return horaStr === hora;
    });

    if (fecha === '2025-11-24' && hora === '08' && horarioEncontrado) {
        console.log('✅ ENCONTRADO para', fecha, hora, ':', horarioEncontrado);
    }

    return horarioEncontrado;
}

function buscarTurnoOcupado(fecha, hora) {
    return calendarioState.turnosOcupados.find(turno => {
        const fechaTurno = new Date(turno.fecha_hora);
        const fechaTurnoStr = fechaTurno.toISOString().split('T')[0];
        const horaTurnoStr = fechaTurno.getHours().toString().padStart(2, '0');

        return fechaTurnoStr === fecha && horaTurnoStr === hora;
    });
}

// ==============================================================
// PASO 5: CONFIRMAR
// ============================================================

function mostrarResumenTurno() {
    const pac = appState.pacienteSeleccionado;
    const esp = appState.especialidadSeleccionada;
    const med = appState.medicoSeleccionado;
    const horario = appState.horarioSeleccionado;

    document.getElementById('resumen-paciente').textContent =
        `${pac.nombre} ${pac.apellido} (DNI: ${pac.dni})`;
    document.getElementById('resumen-especialidad').textContent = esp.nombre;
    document.getElementById('resumen-medico').textContent =
        `Dr. ${med.nombre} ${med.apellido}`;
    document.getElementById('resumen-fecha-hora').textContent = formatDateTime(horario);
}

async function confirmarTurno() {
    const motivo = document.getElementById('turno-motivo').value.trim() || null;

    const turnoData = {
        id_paciente: appState.pacienteSeleccionado.id,
        id_medico: appState.medicoSeleccionado.id,
        id_especialidad: appState.especialidadSeleccionada.id,
        fecha_hora: appState.horarioSeleccionado,
        duracion_minutos: 30,
        motivo: motivo,
    };

    console.log('📤 Enviando datos del turno:', turnoData);

    try {
        showLoading();
        const turno = await api.createTurno(turnoData);

        hideLoading();

        showToast('¡Turno reservado exitosamente!', 'success');

        // Mostrar confirmación en un modal o alert
        const mensaje = `
Turno reservado exitosamente

Paciente: ${appState.pacienteSeleccionado.nombre} ${appState.pacienteSeleccionado.apellido}
Especialidad: ${appState.especialidadSeleccionada.nombre}
Médico: Dr. ${appState.medicoSeleccionado.nombre} ${appState.medicoSeleccionado.apellido}
Fecha y Hora: ${formatDateTime(appState.horarioSeleccionado)}

¡Recuerde asistir a su turno!
        `;

        alert(mensaje);

        // Volver al inicio
        navigateTo('home');

    } catch (error) {
        hideLoading();
        showToast(`Error al reservar turno: ${error.message}`, 'error');
    }
}

// ============================================================
// MIS TURNOS
// ============================================================

async function buscarTurnosPaciente() {
    const dni = document.getElementById('buscar-turnos-dni').value.trim();

    if (!dni) {
        showToast('Ingrese un DNI', 'warning');
        return;
    }

    try {
        showLoading();

        // Primero buscar el paciente
        const paciente = await api.getPacienteByDNI(dni);

        // Luego buscar sus turnos
        const turnos = await api.getTurnosPaciente(paciente.id, false);

        mostrarTurnosList(turnos);

    } catch (error) {
        showToast('Error al buscar turnos', 'error');
        document.getElementById('turnos-list').innerHTML =
            '<p style="text-align: center; padding: 2rem;">No se encontraron turnos</p>';
    } finally {
        hideLoading();
    }
}

function mostrarTurnosList(turnos) {
    const list = document.getElementById('turnos-list');
    list.innerHTML = '';

    if (turnos.length === 0) {
        list.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--text-secondary);">No hay turnos registrados</p>';
        return;
    }

    // Ordenar por fecha (más recientes primero)
    turnos.sort((a, b) => new Date(b.fecha_hora) - new Date(a.fecha_hora));

    turnos.forEach(turno => {
        const card = document.createElement('div');
        card.className = `turno-card ${turno.estado.codigo.toLowerCase()}`;

        const estadoClass =
            turno.estado.codigo === 'PEND' ? 'pendiente' :
                turno.estado.codigo === 'CONF' ? 'confirmado' :
                    'cancelado';

        card.innerHTML = `
            <div class="turno-header">
                <h3>${turno.especialidad.nombre}</h3>
                <span class="turno-estado ${estadoClass}">${turno.estado.descripcion}</span>
            </div>
            <div class="turno-details">
                <div class="turno-detail">
                    <i class="fas fa-user-md"></i>
                    <span>Dr. ${turno.medico.nombre_completo}</span>
                </div>
                <div class="turno-detail">
                    <i class="fas fa-calendar-alt"></i>
                    <span>${formatDateTime(turno.fecha_hora)}</span>
                </div>
                <div class="turno-detail">
                    <i class="fas fa-clock"></i>
                    <span>${turno.duracion_minutos} minutos</span>
                </div>
            </div>
            ${turno.motivo ? `<p style="margin-top: 1rem; color: var(--text-secondary);"><strong>Motivo:</strong> ${turno.motivo}</p>` : ''}
            <div class="turno-actions">
                ${turno.estado.codigo === 'PEND' ? `
                    <button class="btn btn-success" onclick="confirmarTurnoById(${turno.id})">
                        <i class="fas fa-check"></i> Confirmar
                    </button>
                ` : ''}
                ${turno.estado.codigo !== 'CANC' && turno.estado.codigo !== 'INAS' ? `
                    <button class="btn btn-danger" onclick="cancelarTurnoById(${turno.id})">
                        <i class="fas fa-times"></i> Cancelar
                    </button>
                ` : ''}
            </div>
        `;

        list.appendChild(card);
    });
}

async function confirmarTurnoById(turnoId) {
    if (!confirm('¿Confirmar este turno?')) {
        return;
    }

    try {
        showLoading();
        await api.confirmarTurno(turnoId);
        showToast('Turno confirmado', 'success');

        // Recargar lista
        await buscarTurnosPaciente();
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

async function cancelarTurnoById(turnoId) {
    if (!confirm('¿Está seguro de cancelar este turno?')) {
        return;
    }

    try {
        showLoading();
        await api.cancelarTurno(turnoId);
        showToast('Turno cancelado', 'success');

        // Recargar lista
        await buscarTurnosPaciente();
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// Event listener para buscar turnos con Enter
document.getElementById('buscar-turnos-dni').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        buscarTurnosPaciente();
    }
});

// ============================================================
// GESTIÓN DE PACIENTES
// ============================================================

async function loadPacientesTable() {
    try {
        showLoading();
        const pacientes = await api.getPacientes();

        const tbody = document.getElementById('pacientes-tbody');
        tbody.innerHTML = '';

        if (pacientes.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 2rem;">No hay pacientes registrados</td></tr>';
            return;
        }

        pacientes.forEach(pac => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${pac.dni}</td>
                <td>${pac.nombre} ${pac.apellido}</td>
                <td>${pac.email}</td>
                <td>${pac.telefono}</td>
                <td>${formatDate(pac.fecha_nacimiento)}</td>
                <td>
                    <button class="btn btn-danger" onclick="eliminarPaciente(${pac.id}, '${pac.nombre} ${pac.apellido}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });

    } catch (error) {
        showToast('Error al cargar pacientes', 'error');
    } finally {
        hideLoading();
    }
}

async function eliminarPaciente(id, nombre) {
    if (!confirm(`¿Está seguro de eliminar al paciente ${nombre}?`)) {
        return;
    }

    try {
        showLoading();
        await api.deletePaciente(id);
        showToast('Paciente eliminado', 'success');
        await loadPacientesTable();
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

function navegarRegistrarPaciente() {
    navigateTo('turnos');
    document.querySelector('[data-tab="nuevo-paciente"]').click();
}

// ============================================================
// GESTIÓN DE MÉDICOS
// ============================================================

async function loadMedicosTable() {
    try {
        showLoading();
        const medicos = await api.getMedicos();

        const tbody = document.getElementById('medicos-tbody');
        tbody.innerHTML = '';

        if (medicos.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 2rem;">No hay médicos registrados</td></tr>';
            return;
        }

        medicos.forEach(med => {
            const row = document.createElement('tr');
            const especialidadesStr = med.especialidades.map(e => e.nombre).join(', ');

            row.innerHTML = `
                <td>${med.matricula}</td>
                <td>${med.nombre} ${med.apellido}</td>
                <td>${especialidadesStr}</td>
                <td>${med.email}</td>
                <td>
                    <button class="btn btn-danger" onclick="eliminarMedico(${med.id}, '${med.nombre} ${med.apellido}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            tbody.appendChild(row);
        });

    } catch (error) {
        showToast('Error al cargar médicos', 'error');
    } finally {
        hideLoading();
    }
}

async function loadEspecialidadesCheckboxes() {
    try {
        const especialidades = await api.getEspecialidades();
        const container = document.getElementById('med-especialidades-check');
        container.innerHTML = '';

        especialidades.forEach(esp => {
            const label = document.createElement('label');
            label.className = 'checkbox-label';
            label.innerHTML = `
                <input type="checkbox" name="especialidades" value="${esp.id}">
                ${esp.nombre}
            `;
            container.appendChild(label);
        });

    } catch (error) {
        console.error('Error al cargar especialidades:', error);
    }
}

// Formulario de nuevo médico
const formMedico = document.getElementById('form-nuevo-medico');
if (formMedico) {
    formMedico.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Obtener especialidades seleccionadas
        const checkboxes = document.querySelectorAll('input[name="especialidades"]:checked');
        const especialidadesIds = Array.from(checkboxes).map(cb => parseInt(cb.value));

        if (especialidadesIds.length === 0) {
            showToast('Debe seleccionar al menos una especialidad', 'warning');
            return;
        }

        const medicoData = {
            matricula: document.getElementById('med-matricula').value.trim(),
            dni: document.getElementById('med-dni').value.trim(),
            nombre: document.getElementById('med-nombre').value.trim(),
            apellido: document.getElementById('med-apellido').value.trim(),
            email: document.getElementById('med-email').value.trim(),
            telefono: document.getElementById('med-telefono').value.trim(),
            especialidades_ids: especialidadesIds
        };

        try {
            showLoading();
            await api.createMedico(medicoData);

            showToast('Médico registrado exitosamente', 'success');
            formMedico.reset();

            // Volver a la lista
            document.querySelector('[data-tab="lista-medicos"]').click();
            loadMedicosTable();

        } catch (error) {
            showToast(`Error al registrar médico: ${error.message}`, 'error');
        } finally {
            hideLoading();
        }
    });
}

async function eliminarMedico(id, nombre) {
    if (!confirm(`¿Está seguro de eliminar al Dr. ${nombre}?`)) {
        return;
    }

    try {
        showLoading();
        await api.deleteMedico(id);
        showToast('Médico eliminado exitosamente', 'success');
        loadMedicosTable();
    } catch (error) {
        showToast(`Error al eliminar médico: ${error.message}`, 'error');
    } finally {
        hideLoading();
    }
}

// ============================================================
// INICIALIZACIÓN
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    console.log('Sistema de Turnos Médicos - Inicializado');
    loadHomeStats();
});
