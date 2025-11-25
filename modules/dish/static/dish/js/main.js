/**
 * Dish Module Entry Point
 * Imports all dish-related CSS and JS
 */

// Import dish styles
import '../css/list.css';
import '../css/detail.css';

// Import shared styles
import '@shared/css/variables.css';
import '@shared/css/base.css';
import '@shared/css/components.css';
import '@shared/css/filters.css';
import '@shared/css/cards.css';
import '@shared/css/buttons.css';

// Import dish functionality
import './filters.js';
import './list.js';
import './infinite-scroll.js';
import './card-initializer.js';
