# Calendario Semanal de Turnos Médicos

## 🎨 Nuevo Diseño Implementado

Se ha implementado una vista de calendario semanal moderna e intuitiva para la selección de turnos médicos, similar a un calendario académico.

## ✨ Características

### Vista de Calendario
- **Tabla semanal**: Muestra 7 días de la semana (Lunes a Domingo)
- **Franjas horarias**: Desde las 8:00 hasta las 20:00 en bloques de 1 hora
- **Colores diferenciados**: 
  - Blanco: Horarios disponibles
  - Azul: Turnos ocupados estándar
  - Amarillo: Turnos ocupados (variante)
  - Verde: Turnos ocupados (variante)
  - Rosa: Turnos ocupados (variante)
  - Azul oscuro: Horario seleccionado

### Interacción
- **Click para seleccionar**: Haga clic en cualquier celda blanca (disponible) para seleccionar el horario
- **Hover effect**: Las celdas disponibles muestran un efecto visual al pasar el cursor
- **Indicador de selección**: La celda seleccionada se destaca en color azul oscuro

### Navegación
- **Navegación semanal**: Botones para avanzar o retroceder semanas
- **Indicador de semana actual**: Muestra el rango de fechas de la semana visible
- **Leyenda**: Explica el significado de cada color

### Información en Celdas Ocupadas
Cada celda ocupada muestra:
- Hora del turno
- Estado ("Turno Reservado")
- Nombre del paciente

## 🚀 Cómo Usar

1. **Navegue al paso de selección de horario** en el proceso de reserva de turnos
2. **Seleccione la semana deseada** usando los botones de navegación
3. **Haga clic en un horario disponible** (celda blanca)
4. **Confirme su selección** y continúe con el proceso

## 📱 Responsive Design

El calendario se adapta a diferentes tamaños de pantalla:
- **Desktop**: Vista completa con todas las columnas visibles
- **Tablet**: Scroll horizontal disponible
- **Mobile**: Scroll horizontal con fuente reducida

## 🎯 Funcionalidades Técnicas

### Estado del Calendario
```javascript
calendarioState = {
    semanaActual: 0,           // 0 = semana actual, 1 = siguiente
    horariosTodos: {},         // Horarios disponibles del médico
    turnosOcupados: []         // Turnos ya reservados
}
```

### Funciones Principales
- `cargarHorariosDisponibles()`: Carga datos desde la API
- `renderizarCalendarioSemanal()`: Dibuja el calendario
- `cambiarSemana(direccion)`: Navega entre semanas
- `buscarHorarioDisponible()`: Encuentra disponibilidad
- `buscarTurnoOcupado()`: Verifica turnos existentes

## 🔧 Personalización

### Modificar Rango de Horas
En `app.js`, línea ~585:
```javascript
// Cambiar de 8-20 a 7-22, por ejemplo
for (let hora = 7; hora <= 22; hora++) {
    horasDelDia.push(`${hora.toString().padStart(2, '0')}:00`);
}
```

### Modificar Colores
En `styles.css`, sección "Calendario Semanal":
```css
.cal-celda.ocupado {
    background: linear-gradient(135deg, #TU_COLOR_1, #TU_COLOR_2);
}
```

## 📊 Mejoras Futuras Sugeridas

1. **Vista mensual**: Alternar entre vista semanal y mensual
2. **Filtros avanzados**: Por especialidad, médico, duración
3. **Tooltip mejorado**: Más información al hacer hover
4. **Exportar calendario**: Descargar como PDF o ICS
5. **Vista de múltiples médicos**: Comparar disponibilidad

## 🐛 Solución de Problemas

### El calendario no se carga
- Verifique que el médico tenga disponibilidades configuradas
- Revise la consola del navegador para errores de API
- Asegúrese de que el backend esté ejecutándose

### No se muestran turnos ocupados
- Verifique que existan turnos en la base de datos
- El endpoint `/turnos/medico/{id}` debe estar funcionando

### Los colores no se ven bien
- Limpie la caché del navegador
- Verifique que `styles.css` se esté cargando correctamente

## 📝 Notas de Implementación

- Compatible con todos los navegadores modernos
- Utiliza CSS Grid para el layout
- Implementado con JavaScript vanilla (sin frameworks)
- Totalmente integrado con el sistema existente
