/**
 * Gestión de filtros para el listado de categorías
 * Responsabilidad única: Manejo de la interacción con los filtros de categorías
 */

document.addEventListener('DOMContentLoaded', function() {
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

    // Debounce para búsqueda en tiempo real (opcional)
    if (searchInput && filterForm) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Comentado para usar solo el botón de búsqueda
                // filterForm.submit();
            }, 500);
        });
    }
}

/**
 * Envía el formulario de filtros de categorías
 * @param {HTMLFormElement} form - El formulario a enviar
 */
function submitCategoryFilterForm(form) {
    if (form) {
        form.submit();
    }
}
