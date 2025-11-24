// Función para cargar calendario de turnos disponibles
async function cargarHorariosDisponibles() {
    try {
        showLoading();
        
        // Obtener calendario completo del médico
        const calendario = await api.getCalendarioDisponibilidad(appState.medicoSeleccionado.id, 14, 30);
        
        const container = document.getElementById('calendario-turnos');
        container.innerHTML = '';
        
        if (Object.keys(calendario).length === 0) {
            container.innerHTML = '<p style="text-align: center; padding: 3rem; color: var(--text-secondary);">No hay horarios disponibles en los próximos 14 días</p>';
            return;
        }
        
        // Agrupar por fecha y crear cards
        const fechas = Object.keys(calendario).sort();
        
        fechas.forEach(fecha => {
            const horarios = calendario[fecha];
            
            // Crear card de fecha
            const fechaCard = document.createElement('div');
            fechaCard.className = 'fecha-card';
            
            // Header con la fecha
            const header = document.createElement('div');
            header.className = 'fecha-header';
            const fechaObj = new Date(fecha + 'T00:00:00');
            const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            header.innerHTML = `
                <i class="fas fa-calendar-day"></i>
                <span>${fechaObj.toLocaleDateString('es-AR', options)}</span>
                <span class="badge-count">${horarios.length} turnos</span>
            `;
            fechaCard.appendChild(header);
            
            // Grid de horarios
            const horariosGrid = document.createElement('div');
            horariosGrid.className = 'horarios-mini-grid';
            
            horarios.forEach(horarioISO => {
                const horarioBtn = document.createElement('button');
                horarioBtn.className = 'horario-mini-btn';
                
                const horarioObj = new Date(horarioISO);
                const horaStr = horarioObj.toLocaleTimeString('es-AR', {
                    hour: '2-digit',
                    minute: '2-digit'
                });
                
                horarioBtn.textContent = horaStr;
                horarioBtn.onclick = () => {
                    // Desmarcar todos
                    document.querySelectorAll('.horario-mini-btn').forEach(b => 
                        b.classList.remove('selected')
                    );
                    
                    // Marcar este
                    horarioBtn.classList.add('selected');
                    appState.horarioSeleccionado = horarioISO;
                    document.getElementById('btn-step-4').disabled = false;
                };
                
                horariosGrid.appendChild(horarioBtn);
            });
            
            fechaCard.appendChild(horariosGrid);
            container.appendChild(fechaCard);
        });
        
    } catch (error) {
        console.error('Error al cargar calendario:', error);
        showToast('Error al cargar horarios disponibles', 'error');
        document.getElementById('calendario-turnos').innerHTML = 
            '<p style="text-align: center; padding: 3rem; color: var(--danger-color);">Error al cargar horarios</p>';
    } finally {
        hideLoading();
    }
}
