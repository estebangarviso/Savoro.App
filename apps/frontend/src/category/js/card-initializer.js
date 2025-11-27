/**
 * Card Initializer - Automatically initialize cards using MutationObserver
 * This watches for new cards being added to the DOM and initializes them
 */
import { initializeCategoryCard } from './list.js';

// Use MutationObserver to automatically initialize new cards
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      // Check if the added node is a card or contains cards
      if (node.nodeType === Node.ELEMENT_NODE) {
        if (node.classList && node.classList.contains('card-grid')) {
          initializeCategoryCard(node);
        } else {
          // Check for cards within the added node
          const cards = node.querySelectorAll('.card-grid');
          cards.forEach((card) => initializeCategoryCard(card));
        }
      }
    });
  });
});

// Start observing when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  const categoryGrid = document.getElementById('categoryGrid');
  if (categoryGrid) {
    observer.observe(categoryGrid, {
      childList: true,
      subtree: true,
    });
  }
});
