/**
 * Card Initializer - Automatically initialize cards using MutationObserver
 * This watches for new cards being added to the DOM and initializes them
 */
import { initializeDishCard } from './list.js';

// Use MutationObserver to automatically initialize new cards
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      // Check if the added node is a card or contains cards
      if (node.nodeType === Node.ELEMENT_NODE) {
        if (
          node.classList &&
          (node.classList.contains('card-grid') || node.classList.contains('dish-card'))
        ) {
          initializeDishCard(node);
        } else {
          // Check for cards within the added node
          const cards = node.querySelectorAll('.card-grid, .dish-card');
          cards.forEach((card) => initializeDishCard(card));
        }
      }
    });
  });
});

// Start observing when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const dishGrid = document.getElementById('dishGrid');
  if (dishGrid) {
    observer.observe(dishGrid, {
      childList: true,
      subtree: true,
    });
  }
});
