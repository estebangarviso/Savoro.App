/**
 * Dish List - Delete and UI interactions
 */
import M from 'materialize-css';
import { displayToast } from '@shared/js/messages.js';

let dishToDelete = null;
let modal = null;

/**
 * Initialize card events (click to navigate, delete, edit)
 * Call this for each card when it's rendered
 */
export function initializeDishCard(cardElement) {
  if (!cardElement || cardElement.dataset.eventsAttached === 'true') return;

  // Navigate to detail on card click
  cardElement.addEventListener('click', function (e) {
    // Don't navigate if clicking on action buttons
    if (
      !e.target.closest('.delete-dish-btn') &&
      !e.target.closest('.delete-btn-floating') &&
      !e.target.closest('.delete-dish-btn-floating') &&
      !e.target.closest('.edit-btn-floating') &&
      !e.target.closest('.edit-dish-btn-floating') &&
      !e.target.closest('.btn-floating')
    ) {
      const href = this.dataset.href;
      if (href) {
        window.location.href = href;
      }
    }
  });

  // Handle delete button
  const deleteBtn = cardElement.querySelector('.delete-dish-btn');
  if (deleteBtn) {
    deleteBtn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();

      dishToDelete = {
        id: this.dataset.dishId,
        name: this.dataset.dishName,
      };

      document.getElementById('dishNameToDelete').textContent = dishToDelete.name;

      if (modal) {
        modal.open();
      }
    });
  }

  // Mark as initialized
  cardElement.dataset.eventsAttached = 'true';
}

/**
 * Initialize all dish cards in the container
 */
export function initializeAllDishCards(container = document) {
  const cards = container.querySelectorAll('.card-grid, .dish-card');
  cards.forEach((card) => initializeDishCard(card));
}

document.addEventListener('DOMContentLoaded', function () {
  // Initialize modals
  const modalElems = document.querySelectorAll('.modal');
  M.Modal.init(modalElems);

  const deleteDishModal = document.getElementById('deleteDishModal');
  modal = M.Modal.getInstance(deleteDishModal);

  // Initialize existing cards
  initializeAllDishCards();

  // Handle confirm delete
  document.getElementById('confirmDeleteDishBtn').addEventListener('click', function () {
    if (!dishToDelete) return;

    // Get CSRF token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Send DELETE request
    fetch(`/dishes/${dishToDelete.id}/delete/`, {
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

          // Remove the dish card from DOM
          const dishCard = document
            .querySelector(`[data-dish-id="${dishToDelete.id}"]`)
            .closest('.col');
          if (dishCard) {
            dishCard.style.opacity = '0';
            setTimeout(() => dishCard.remove(), 300);
          }
        } else {
          // Show error toast
          displayToast(data.message, 'error');
        }

        dishToDelete = null;
      })
      .catch((error) => {
        modal.close();
        displayToast('Error al eliminar el plato', 'error');
        console.error('Error:', error);
      });
  });
});
