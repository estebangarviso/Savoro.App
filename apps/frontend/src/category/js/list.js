/**
 * Category List - Delete and UI interactions
 */
import M from 'materialize-css';
import { displayToast } from '@shared/js/messages.js';

let categoryToDelete = null;
let modal = null;

/**
 * Initialize card events (click to navigate)
 * Call this for each card when it's rendered
 */
export function initializeCategoryCard(cardElement) {
  if (!cardElement || cardElement.dataset.eventsAttached === 'true') return;

  // Navigate to detail on card click
  cardElement.addEventListener('click', function (e) {
    // Don't navigate if clicking on action buttons
    if (
      !e.target.closest('.delete-category-btn') &&
      !e.target.closest('.delete-btn-floating') &&
      !e.target.closest('.edit-btn-floating') &&
      !e.target.closest('.btn-floating')
    ) {
      const href = this.dataset.href;
      if (href) {
        window.location.href = href;
      }
    }
  });

  // Handle delete button
  const deleteBtn = cardElement.querySelector('.delete-category-btn');
  if (deleteBtn) {
    deleteBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      categoryToDelete = {
        id: this.dataset.categoryId,
        name: this.dataset.categoryName,
        hasDishes: parseInt(this.dataset.hasDishes) > 0,
      };

      document.getElementById('categoryNameToDelete').textContent = categoryToDelete.name;

      if (categoryToDelete.hasDishes) {
        document.getElementById('categoryWarning').innerHTML =
          '<i class="material-icons tiny left red-text">warning</i>Esta categoría tiene ' +
          this.dataset.hasDishes +
          ' plato(s) asociado(s). No podrá ser eliminada.';
      } else {
        document.getElementById('categoryWarning').textContent =
          'Esta acción marcará la categoría como eliminada.';
      }

      if (modal) {
        modal.open();
      }
    });
  }

  // Mark as initialized
  cardElement.dataset.eventsAttached = 'true';
}

/**
 * Initialize all category cards in the container
 */
export function initializeAllCategoryCards(container = document) {
  const cards = container.querySelectorAll('.card-grid');
  cards.forEach((card) => initializeCategoryCard(card));
}

document.addEventListener('DOMContentLoaded', function () {
  // Initialize modals
  const modalElems = document.querySelectorAll('.modal');
  M.Modal.init(modalElems);

  const deleteCategoryModal = document.getElementById('deleteCategoryModal');
  modal = M.Modal.getInstance(deleteCategoryModal);

  // Initialize existing cards
  initializeAllCategoryCards();

  // Handle confirm delete
  document.getElementById('confirmDeleteBtn').addEventListener('click', function () {
    if (!categoryToDelete) return;

    // Get CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send DELETE request
    fetch(`/categories/${categoryToDelete.id}/delete/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken,
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => {
        modal.close();

        if (data.success) {
          // Show success toast
          displayToast(data.message, 'success');

          // Remove the category card from DOM
          const categoryCard = document
            .querySelector(`[data-category-id="${categoryToDelete.id}"]`)
            .closest('.col');
          if (categoryCard) {
            categoryCard.style.opacity = '0';
            setTimeout(() => categoryCard.remove(), 300);
          }
        } else {
          // Show error toast
          displayToast(data.message, 'error');
        }

        categoryToDelete = null;
      })
      .catch((error) => {
        modal.close();
        displayToast('Error al eliminar la categoría', 'error');
        console.error('Error:', error);
      });
  });
});
