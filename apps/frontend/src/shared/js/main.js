/**
 * Shared JavaScript Entry Point
 * Initializes Materialize CSS and provides global utilities
 */

// Import Materialize CSS and JS
import 'materialize-css/dist/css/materialize.min.css';
import M from 'materialize-css';

// Import shared modules
import { displayToast } from './messages.js';

// Initialize Materialize components globally
document.addEventListener('DOMContentLoaded', function () {
  // Auto-initialize all Materialize components
  M.AutoInit();

  // Initialize specific components that need custom config
  const sidenavElems = document.querySelectorAll('.sidenav');
  M.Sidenav.init(sidenavElems);

  const selectElems = document.querySelectorAll('select');
  M.FormSelect.init(selectElems);

  const modalElems = document.querySelectorAll('.modal');
  M.Modal.init(modalElems);
});

export { M, displayToast };
