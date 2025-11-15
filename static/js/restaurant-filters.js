/**
 * Gestión de filtros para el listado de platos
 * Responsabilidad única: Manejo de la interacción con los filtros
 */

document.addEventListener('DOMContentLoaded', function() {
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
    const filterForm = document.getElementById('filterForm');

    if (categorySelect && filterForm) {
        categorySelect.addEventListener('change', () => submitFilterForm(filterForm));
    }

    if (tagSelect && filterForm) {
        tagSelect.addEventListener('change', () => submitFilterForm(filterForm));
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
