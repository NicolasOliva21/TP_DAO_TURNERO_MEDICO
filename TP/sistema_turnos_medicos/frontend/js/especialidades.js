/**
 * Módulo de Gestión de Especialidades
 */

// Estado del módulo
const especialidadesState = {
    especialidades: [],
    especialidadEditando: null,
    modoEdicion: false
};

// ============================================================
// INICIALIZACIÓN
// ============================================================

async function initEspecialidades() {
    console.log('[Especialidades] Inicializando módulo...');
    await cargarEspecialidades();
    setupEventListenersEspecialidades();
    console.log('[Especialidades] Módulo inicializado');
}

function setupEventListenersEspecialidades() {
    const btnNueva = document.getElementById('btn-nueva-especialidad');
    if (btnNueva) {
        btnNueva.addEventListener('click', mostrarModalNuevaEspecialidad);
    }

    const form = document.getElementById('form-especialidad');
    if (form) {
        form.addEventListener('submit', guardarEspecialidad);
    }
}

// ============================================================
// CARGA Y RENDERIZADO
// ============================================================

async function cargarEspecialidades() {
    try {
        showLoading();
        
        const especialidades = await api.getEspecialidades();
        especialidadesState.especialidades = especialidades;
        
        renderizarTablaEspecialidades();
        
    } catch (error) {
        console.error('[Especialidades] Error al cargar:', error);
        showToast('Error al cargar especialidades', 'error');
    } finally {
        hideLoading();
    }
}

function renderizarTablaEspecialidades() {
    const tbody = document.getElementById('especialidades-tbody');
    if (!tbody) return;

    if (especialidadesState.especialidades.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" style="text-align: center; padding: 2rem; color: var(--text-muted);">
                    No hay especialidades registradas
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = especialidadesState.especialidades.map(esp => `
        <tr>
            <td>${esp.id}</td>
            <td><strong>${esp.nombre}</strong></td>
            <td>${esp.descripcion || '<em class="text-muted">Sin descripción</em>'}</td>
            <td>
                <div class="actions">
                    <button class="btn-icon btn-edit" onclick="editarEspecialidad(${esp.id})" title="Editar">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-icon btn-delete" onclick="eliminarEspecialidad(${esp.id})" title="Eliminar">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// ============================================================
// MODAL
// ============================================================

function mostrarModalNuevaEspecialidad() {
    especialidadesState.modoEdicion = false;
    especialidadesState.especialidadEditando = null;

    const modal = document.getElementById('modal-especialidad');
    const form = document.getElementById('form-especialidad');
    const titulo = document.getElementById('especialidad-modal-titulo');

    if (!modal || !form || !titulo) return;

    form.reset();
    titulo.textContent = 'Nueva Especialidad';
    modal.style.display = 'flex';
}

function cerrarModalEspecialidad() {
    const modal = document.getElementById('modal-especialidad');
    const form = document.getElementById('form-especialidad');

    if (modal) modal.style.display = 'none';
    if (form) form.reset();

    especialidadesState.modoEdicion = false;
    especialidadesState.especialidadEditando = null;
}

// ============================================================
// CRUD OPERATIONS
// ============================================================

async function guardarEspecialidad(event) {
    event.preventDefault();

    const nombre = document.getElementById('especialidad-nombre').value.trim();
    const descripcion = document.getElementById('especialidad-descripcion').value.trim();

    const data = {
        nombre,
        descripcion: descripcion || null
    };

    try {
        showLoading();

        if (especialidadesState.modoEdicion) {
            // Actualizar
            await api.updateEspecialidad(especialidadesState.especialidadEditando, data);
            showToast('Especialidad actualizada correctamente', 'success');
        } else {
            // Crear
            await api.createEspecialidad(data);
            showToast('Especialidad creada correctamente', 'success');
        }

        cerrarModalEspecialidad();
        await cargarEspecialidades();

    } catch (error) {
        console.error('[Especialidades] Error al guardar:', error);
        const mensaje = error.message || 'Error al guardar la especialidad';
        showToast(mensaje, 'error');
    } finally {
        hideLoading();
    }
}

async function editarEspecialidad(id) {
    const especialidad = especialidadesState.especialidades.find(e => e.id === id);
    if (!especialidad) return;

    especialidadesState.modoEdicion = true;
    especialidadesState.especialidadEditando = id;

    const modal = document.getElementById('modal-especialidad');
    const titulo = document.getElementById('especialidad-modal-titulo');

    document.getElementById('especialidad-nombre').value = especialidad.nombre;
    document.getElementById('especialidad-descripcion').value = especialidad.descripcion || '';

    if (titulo) titulo.textContent = 'Editar Especialidad';
    if (modal) modal.style.display = 'flex';
}

async function eliminarEspecialidad(id) {
    const especialidad = especialidadesState.especialidades.find(e => e.id === id);
    if (!especialidad) return;

    const confirmacion = confirm(
        `¿Está seguro de eliminar la especialidad "${especialidad.nombre}"?\n\n` +
        `Esta acción no se puede deshacer y fallará si hay médicos asociados.`
    );

    if (!confirmacion) return;

    try {
        showLoading();
        
        await api.deleteEspecialidad(id);
        showToast('Especialidad eliminada correctamente', 'success');
        await cargarEspecialidades();

    } catch (error) {
        console.error('[Especialidades] Error al eliminar:', error);
        const mensaje = error.message || 'Error al eliminar la especialidad';
        showToast(mensaje, 'error');
    } finally {
        hideLoading();
    }
}

// ============================================================
// EXPORTAR FUNCIONES GLOBALES
// ============================================================

window.initEspecialidades = initEspecialidades;
window.editarEspecialidad = editarEspecialidad;
window.eliminarEspecialidad = eliminarEspecialidad;
window.cerrarModalEspecialidad = cerrarModalEspecialidad;
