/**
 * Gestión de filtros para el listado de categorías
 * Responsabilidad única: Manejo de la interacción con los filtros de categorías
 */
import M from 'materialize-css';

document.addEventListener('DOMContentLoaded', function () {
  initializeCategoryFilters();
});

/**
 * Inicializa los componentes de filtros de categorías
 */
function initializeCategoryFilters() {
  attachCategoryFilterEventListeners();
}

/**
 * Adjunta los event listeners a los elementos de filtro
 */
function attachCategoryFilterEventListeners() {
  const filterForm = document.getElementById('categoryFilterForm');
  const searchInput = document.getElementById('categorySearch');
  const searchButton = filterForm?.querySelector('button[type="submit"]');
  const clearButton = filterForm?.querySelector('a[href*="category:list"]');

  // Evento de submit del formulario
  if (filterForm) {
    filterForm.addEventListener('submit', function (e) {
      // El formulario se enviará naturalmente con method="get"
      // No necesitamos prevenir el comportamiento por defecto
    });
  }

  // Evento para el botón de limpiar
  if (clearButton) {
    clearButton.addEventListener('click', function (e) {
      // El href ya redirige correctamente
      // No necesitamos hacer nada adicional
    });
  }

  // Permitir búsqueda con Enter
  if (searchInput) {
    searchInput.addEventListener('keypress', function (e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (filterForm) {
          filterForm.submit();
        }
      }
    });
  }
}
