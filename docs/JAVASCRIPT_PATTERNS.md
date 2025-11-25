# JavaScript Patterns & Best Practices

## Arquitectura Modular

Este proyecto utiliza módulos ES6 y evita contaminar el scope global (`window`) siguiendo las mejores prácticas de desarrollo moderno.

## Patrones Implementados

### 1. Custom Events para Comunicación

En lugar de exponer funciones en `window`, usamos **Custom Events** para la comunicación entre templates y módulos JavaScript.

#### Ejemplo: Sistema de Toast Notifications

**❌ Mal - Contaminando el scope global:**
```javascript
// messages.js
export function displayToast(message, tag) { ... }
window.displayToast = displayToast; // ❌ Mala práctica

// En template
<script>
  displayToast('Hello', 'success'); // Depende de window
</script>
```

**✅ Bien - Usando Custom Events:**
```javascript
// messages.js
export function displayToast(message, tag) { ... }

document.addEventListener('toast:show', (event) => {
  const { message, tag } = event.detail;
  displayToast(message, tag);
});

// En template
<script>
  document.dispatchEvent(new CustomEvent('toast:show', {
    detail: { message: 'Hello', tag: 'success' }
  }));
</script>
```

**Ventajas:**
- ✅ No contamina el scope global
- ✅ Comunicación desacoplada
- ✅ Fácil de testear
- ✅ Sigue estándares web modernos

### 2. MutationObserver para Componentes Dinámicos

Para inicializar eventos en elementos cargados dinámicamente (AJAX, infinite scroll), usamos **MutationObserver**.

#### Ejemplo: Inicialización de Cards

**❌ Mal - Event Delegation Global:**
```javascript
// Problema: eventos duplicados, difícil de mantener
document.addEventListener('click', function(e) {
  if (e.target.matches('.card')) {
    // handle click
  }
});
```

**✅ Bien - MutationObserver + Inicialización Individual:**
```javascript
// card-initializer.js
import { initializeCard } from './list.js';

const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      if (node.nodeType === Node.ELEMENT_NODE) {
        if (node.classList.contains('card')) {
          initializeCard(node);
        } else {
          const cards = node.querySelectorAll('.card');
          cards.forEach((card) => initializeCard(card));
        }
      }
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('cardContainer');
  if (container) {
    observer.observe(container, { childList: true, subtree: true });
  }
});

// list.js
export function initializeCard(cardElement) {
  if (cardElement.dataset.eventsAttached === 'true') return;
  
  cardElement.addEventListener('click', function(e) {
    // handle click
  });
  
  cardElement.dataset.eventsAttached = 'true';
}
```

**Ventajas:**
- ✅ Detecta automáticamente nuevos elementos
- ✅ Evita duplicación de eventos
- ✅ Funciona con contenido dinámico (infinite scroll, AJAX)
- ✅ No requiere re-inicializar manualmente

### 3. Módulos ES6 con Path Aliases

Usamos módulos ES6 con alias de rutas para imports limpios:

```javascript
// ❌ Mal
import { displayToast } from '../../../../shared/static/shared/js/messages.js';

// ✅ Bien
import { displayToast } from '@shared/js/messages.js';
```

**Configuración en `vite.config.js`:**
```javascript
resolve: {
  alias: {
    '@shared': path.resolve(__dirname, 'shared/static/shared'),
    '@modules': path.resolve(__dirname, 'modules')
  }
}
```

### 4. Evitar Inline Scripts en Templates

**❌ Mal:**
```html
<div id="card-{{ id }}">
  <script>
    if (window.initCard) {
      window.initCard(document.getElementById('card-{{ id }}'));
    }
  </script>
</div>
```

**✅ Bien:**
```html
<div class="card" data-href="...">
  <!-- Sin scripts inline -->
</div>
<!-- MutationObserver detecta y inicializa automáticamente -->
```

## Reglas de Oro

1. **NUNCA** exponer funciones en `window`
2. **SIEMPRE** usar módulos ES6 con `import/export`
3. **PREFERIR** Custom Events para comunicación template ↔ JS
4. **USAR** MutationObserver para contenido dinámico
5. **EVITAR** scripts inline en templates
6. **MANTENER** el scope global limpio

## Estructura de Archivos

```
modules/
  category/
    static/category/js/
      main.js              # Entry point, importa todo
      list.js              # Lógica de listado y eventos
      card-initializer.js  # MutationObserver para cards
      infinite-scroll.js   # Infinite scroll
      filters.js           # Filtros
shared/
  static/shared/js/
    main.js                # Entry point compartido
    messages.js            # Sistema de toast con Custom Events
```

## Testing

Esta arquitectura facilita el testing:

```javascript
// test/messages.test.js
import { displayToast } from '@shared/js/messages.js';

test('displayToast shows success message', () => {
  displayToast('Success!', 'success');
  // Assert toast appears
});

test('custom event triggers toast', () => {
  document.dispatchEvent(new CustomEvent('toast:show', {
    detail: { message: 'Test', tag: 'info' }
  }));
  // Assert toast appears
});
```

## Referencias

- [MDN - Custom Events](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent)
- [MDN - MutationObserver](https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver)
- [JavaScript Modules Best Practices](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
