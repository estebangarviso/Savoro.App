/**
 * Gestión de filtros para el listado de platos
 * Responsabilidad única: Manejo de la interacción con los filtros
 */
import M from 'materialize-css';

document.addEventListener('DOMContentLoaded', function () {
  initializeFilters();
});

/**
 * Inicializa los componentes de filtros
 */
function initializeFilters() {
  initializeMaterializeSelects();
  attachFilterEventListeners();
}

/**
 * Inicializa los selectores de Materialize CSS
 */
function initializeMaterializeSelects() {
  const selects = document.querySelectorAll('select');
  M.FormSelect.init(selects);
}

/**
 * Adjunta los event listeners a los elementos de filtro
 */
function attachFilterEventListeners() {
  const categorySelect = document.getElementById('category');
  const tagSelect = document.getElementById('tag');
  const searchInput = document.getElementById('search');
  const filterForm = document.getElementById('filterForm');
  const searchButton = filterForm?.querySelector('button[type="submit"]');
  const clearButton = filterForm?.querySelector('a[href*="dish:list"]');

  // Evento de submit del formulario
  if (filterForm) {
    filterForm.addEventListener('submit', function (e) {
      // El formulario se enviará naturalmente con method="get"
      // No necesitamos prevenir el comportamiento por defecto
    });
  }

  // Auto-submit cuando cambia la categoría
  if (categorySelect && filterForm) {
    categorySelect.addEventListener('change', () => submitFilterForm(filterForm));
  }

  // Auto-submit cuando cambia el tag
  if (tagSelect && filterForm) {
    tagSelect.addEventListener('change', () => submitFilterForm(filterForm));
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

  // Evento para el botón de limpiar
  if (clearButton) {
    clearButton.addEventListener('click', function (e) {
      // El href ya redirige correctamente
      // No necesitamos hacer nada adicional
    });
  }
}

/**
 * Envía el formulario de filtros
 * @param {HTMLFormElement} form - El formulario a enviar
 */
function submitFilterForm(form) {
  if (form) {
    form.submit();
  }
}
