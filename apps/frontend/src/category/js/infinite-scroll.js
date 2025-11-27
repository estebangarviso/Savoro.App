/**
 * Infinite Scroll functionality for category list
 * Loads more categories as user scrolls down
 */
import { initializeAllCategoryCards } from './list.js';

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
  const hasNextAttr = document.querySelector('#categoryGrid')?.dataset.hasNext;
  hasMore = hasNextAttr === 'True' || hasNextAttr === 'true';

  // Set up scroll listener
  window.addEventListener('scroll', handleScroll);

  // Set up filter form to reset pagination
  const filterForm = document.getElementById('categoryFilterForm');
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
    loadMoreCategories();
  }
}

/**
 * Load more categories via AJAX
 */
function loadMoreCategories() {
  if (isLoading || !hasMore) return;

  isLoading = true;
  currentPage += 1;

  // Show loading indicator (using Materialize hide/show classes)
  const loadingIndicator = document.getElementById('loadingIndicator');
  if (loadingIndicator) {
    loadingIndicator.classList.remove('hide');
  }

  // Get current search query
  const urlParams = new URLSearchParams(window.location.search);
  const searchQuery = urlParams.get('search') || '';
  const statusFilter = urlParams.get('status') || '';

  // Build URL with pagination
  const url = new URL(window.location.href);
  url.searchParams.set('page', currentPage);
  if (searchQuery) {
    url.searchParams.set('search', searchQuery);
  }
  if (statusFilter) {
    url.searchParams.set('status', statusFilter);
  }

  // Fetch more categories
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
      const categoryGrid = document.getElementById('categoryGrid');
      if (categoryGrid && data.html) {
        // Insert the new content
        categoryGrid.insertAdjacentHTML('beforeend', data.html);

        // Initialize events for all new cards
        initializeAllCategoryCards(categoryGrid);
      }

      // Update pagination state
      hasMore = data.has_next;
      isLoading = false;
    })
    .catch((error) => {
      console.error('Error loading more categories:', error);
      if (loadingIndicator) {
        loadingIndicator.classList.add('hide');
      }
      isLoading = false;
    });
}

export { initializeInfiniteScroll };
