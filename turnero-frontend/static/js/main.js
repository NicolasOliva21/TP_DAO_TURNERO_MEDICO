function openModal(){ const m=document.getElementById('modal'); m.classList.add('open'); }
function closeModal(){ const m=document.getElementById('modal'); m.classList.remove('open'); }
window.openModal = openModal; window.closeModal = closeModal;

document.addEventListener('htmx:afterSwap', (e) => {
  if (e.detail.target && (e.detail.target.id === 'patients-table' || e.detail.target.id === 'doctors-table')) closeModal();
});
