/**
 * Infinite Scroll functionality for dish list
 * Loads more dishes as user scrolls down
 */
import { initializeAllDishCards } from './list.js';

let isLoading = false;
let hasMore = true;
let currentPage = 1;

document.addEventListener('DOMContentLoaded', function () {
  initializeInfiniteScroll();
});

/**
 * Initialize infinite scroll
 */
function initializeInfiniteScroll() {
  // Get has_next from template (set by Django)
  const hasNextAttr = document.querySelector('#dishGrid')?.dataset.hasNext;
  hasMore = hasNextAttr === 'True' || hasNextAttr === 'true';

  // Set up scroll listener
  window.addEventListener('scroll', handleScroll);

  // Set up filter form to reset pagination
  const filterForm = document.getElementById('filterForm');
  if (filterForm) {
    filterForm.addEventListener('submit', function () {
      currentPage = 1;
      hasMore = true;
    });
  }
}

/**
 * Handle scroll event
 */
function handleScroll() {
  if (isLoading || !hasMore) return;

  const scrollPosition = window.innerHeight + window.scrollY;
  const documentHeight = document.documentElement.scrollHeight;
  const threshold = 300; // Load more when 300px from bottom

  if (scrollPosition >= documentHeight - threshold) {
    loadMoreDishes();
  }
}

/**
 * Load more dishes via AJAX
 */
function loadMoreDishes() {
  if (isLoading || !hasMore) return;

  isLoading = true;
  currentPage += 1;

  // Show loading indicator (using Materialize hide/show classes)
  const loadingIndicator = document.getElementById('loadingIndicator');
  if (loadingIndicator) {
    loadingIndicator.classList.remove('hide');
  }

  // Get current filters
  const urlParams = new URLSearchParams(window.location.search);
  const searchQuery = urlParams.get('search') || '';
  const categoryFilter = urlParams.get('category') || '';
  const tagFilter = urlParams.get('tag') || '';

  // Build URL with pagination
  const url = new URL(window.location.href);
  url.searchParams.set('page', currentPage);
  if (searchQuery) url.searchParams.set('search', searchQuery);
  if (categoryFilter) url.searchParams.set('category', categoryFilter);
  if (tagFilter) url.searchParams.set('tag', tagFilter);

  // Fetch more dishes
  fetch(url.toString(), {
    headers: {
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then((response) => response.json())
    .then((data) => {
      // Hide loading indicator
      if (loadingIndicator) {
        loadingIndicator.classList.add('hide');
      }

      // Append new content
      const dishGrid = document.getElementById('dishGrid');
      if (dishGrid && data.html) {
        // Insert HTML directly at the end of dishGrid
        dishGrid.insertAdjacentHTML('beforeend', data.html);

        // Initialize events for all new cards in the container
        initializeAllDishCards(dishGrid);
      }

      // Update pagination state
      hasMore = data.has_next;
      isLoading = false;
    })
    .catch((error) => {
      console.error('Error loading more dishes:', error);
      if (loadingIndicator) {
        loadingIndicator.classList.add('hide');
      }
      isLoading = false;
    });
}

export { initializeInfiniteScroll };
