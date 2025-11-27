/**
 * Messages to Materialize Toasts
 * Converts messages to Materialize toast notifications
 */
import M from 'materialize-css';

/**
 * Display a message as a Materialize toast
 * @param {string} message - The message text
 * @param {string} tag - The message tag (success, error, warning, info)
 */
export function displayToast(message, tag) {
  const icons = {
    error: 'error',
    success: 'check_circle',
    warning: 'warning',
    info: 'info',
  };

  const classes = {
    error: 'red darken-1',
    success: 'green darken-1',
    warning: 'orange darken-1',
    info: 'blue darken-1',
  };

  const icon = icons[tag] || icons.info;
  const cssClass = classes[tag] || classes.info;
  const duration = tag === 'error' ? 5000 : 4000;

  M.toast({
    html: `<i class="material-icons left">${icon}</i>${message}`,
    classes: cssClass,
    displayLength: duration,
  });
}

// Listen for custom events to display toasts
document.addEventListener('toast:show', (event) => {
  const { message, tag } = event.detail;
  displayToast(message, tag);
});
