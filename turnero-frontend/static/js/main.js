function openModal(){ document.getElementById('modal').classList.remove('hidden'); document.getElementById('modal').classList.add('flex'); }
function closeModal(){ document.getElementById('modal').classList.add('hidden'); document.getElementById('modal').classList.remove('flex'); }
window.openModal = openModal; window.closeModal = closeModal;
document.addEventListener('htmx:afterSwap', (e) => {
  // Cerrar modal si se reemplazó la tabla (creación OK)
  if (e.detail.target && e.detail.target.id === 'patients-table') closeModal();
});
