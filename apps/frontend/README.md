# Savoro.App - Frontend (Vite)

<p align="center">
  <img src="https://vitejs.dev/logo.svg" width="120" alt="Vite Logo" />
</p>

<p align="center">
Build system y assets del frontend con Vite + Materialize CSS.
</p>

> **📦 Monorepo**: Este es el frontend. Para el backend Django, ver [`apps/backend/README.md`](../backend/README.md). Para información general, ver el [README principal](../../README.md).

## 📋 Descripción

Este directorio contiene:
- **Build system**: Vite para compilación, optimización y HMR
- **Assets**: JavaScript, CSS, imágenes organizados por módulo
- **Integración Django**: Los assets compilados se sirven desde `staticfiles/`

## 🚀 Inicio Rápido

### Instalación

```bash
# Desde apps/frontend/
pnpm install
```

### Desarrollo

Modo desarrollo con Hot Module Replacement:

```bash
pnpm run dev
```

Servidor Vite disponible en **http://localhost:5173** (solo para preview, la app Django está en puerto 8000).

### Compilación con Vigilancia

Para desarrollo integrado con Django (recompila automáticamente al guardar):

```bash
pnpm run build:watch
```

### Producción

Compilar assets optimizados con minificación y sourcemaps:

```bash
pnpm run build
```

Los archivos compilados se generan en `staticfiles/` y Django los sirve automáticamente.

## 📁 Estructura

```
apps/frontend/
├── src/                    # Código fuente
│   ├── authentication/     # Login/logout JS + CSS
│   ├── category/           # Categorías JS + CSS
│   ├── dish/               # Platos JS + CSS
│   └── shared/             # Componentes compartidos
│       ├── js/             # Utils, messages, navigation
│       └── styles/         # Estilos base, variables
├── staticfiles/            # Output compilado (generado)
│   ├── authentication/
│   ├── category/
│   ├── dish/
│   ├── shared/
│   ├── vendor/             # Materialize, dependencias
│   └── .vite/              # Manifest de Vite
├── vite.config.js          # Configuración de Vite
├── eslint.config.mjs       # Configuración de ESLint
├── package.json            # Dependencias y scripts
└── jsconfig.json           # Configuración de JavaScript
```

## 🛠️ Tecnologías

| Tecnología          | Versión | Propósito                     |
| ------------------- | ------- | ----------------------------- |
| **Vite**            | 5.4+    | Build tool con HMR            |
| **Materialize CSS** | 1.0.0   | Framework UI responsive       |
| **ESLint**          | 9.16+   | Linter para código JavaScript |
| **Prettier**        | 3.4+    | Formateador de código         |

## 📜 Scripts Disponibles

### Build y Desarrollo

| Script                 | Descripción                                            |
| ---------------------- | ------------------------------------------------------ |
| `pnpm run dev`         | Servidor Vite con HMR en `localhost:5173`              |
| `pnpm run build`       | Compilar para producción con minificación y sourcemaps |
| `pnpm run build:watch` | Compilar en modo vigilancia (recompila al guardar)     |
| `pnpm run preview`     | Preview de build de producción en `localhost:4173`     |

### Calidad de Código

| Script                  | Descripción                                |
| ----------------------- | ------------------------------------------ |
| `pnpm run lint`         | Verificar código con ESLint                |
| `pnpm run lint:fix`     | Corregir errores de ESLint automáticamente |
| `pnpm run format`       | Formatear código con Prettier              |
| `pnpm run format:check` | Verificar formato sin modificar archivos   |

## ⚙️ Configuración de Vite

### Entry Points

Vite escanea automáticamente los archivos en:
- `src/*/static/**/*.{js,css}` (módulos individuales)
- `src/shared/static/**/*.{js,css}` (componentes compartidos)

### Output

Los assets compilados se generan en `staticfiles/`:
- **JavaScript minificado**: `*.js`
- **CSS minificado**: `*.css`
- **Sourcemaps**: `*.js.map`, `*.css.map`
- **Manifest**: `.vite/manifest.json` (mapeo de assets)

### Características de Build

- **Tree Shaking**: Elimina código no utilizado
- **Code Splitting**: Lazy loading de módulos
- **Minificación**: ESBuild para optimización rápida
- **Sourcemaps**: Debugging en producción
- **Asset Hashing**: Cache busting con hashes en nombres de archivo

## 🧩 Patrones de Desarrollo

### Custom Events

Comunicación desacoplada entre módulos sin contaminar `window`:

```javascript
// Emitir evento
document.dispatchEvent(new CustomEvent('toast:show', {
  detail: { message: 'Operación exitosa', tag: 'success' }
}));

// Escuchar evento
document.addEventListener('toast:show', (event) => {
  const { message, tag } = event.detail;
  displayToast(message, tag);
});
```

### MutationObserver

Inicialización de componentes dinámicos cargados con AJAX:

```javascript
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      if (node.nodeType === Node.ELEMENT_NODE) {
        if (node.classList.contains('card')) {
          initializeCard(node);
        }
      }
    });
  });
});

observer.observe(document.body, {
  childList: true,
  subtree: true
});
```

Ver [JAVASCRIPT_PATTERNS.md](../../docs/JAVASCRIPT_PATTERNS.md) para patrones completos.

## 🔗 Integración con Django

### Servir Assets

Django sirve los archivos compilados desde `staticfiles/` usando:

```python
# config/settings/base.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.parent.parent / 'apps' / 'frontend' / 'staticfiles']
```

### Incluir en Templates

```django
{% load static %}

<!-- CSS compilado por Vite -->
<link rel="stylesheet" href="{% static 'dish/css/list.css' %}">

<!-- JavaScript compilado por Vite -->
<script type="module" src="{% static 'dish/js/list.js' %}"></script>
```

### Workflow de Desarrollo

1. **Terminal 1**: `pnpm run build:watch` (en `apps/frontend/`)
2. **Terminal 2**: `python manage.py runserver` (en `apps/backend/`)
3. Editar archivos en `apps/frontend/src/`
4. Vite recompila automáticamente
5. Django sirve los nuevos assets

## 🎨 Materialize CSS

Utilizamos Materialize CSS 1.0 para componentes UI:

### Componentes Principales

- **Cards**: Tarjetas de platos y categorías
- **Modals**: Diálogos de confirmación y formularios
- **Toast**: Notificaciones temporales
- **Forms**: Inputs, selects, textareas con validación
- **Navigation**: Navbar, sidenav, breadcrumbs
- **Buttons**: Floating action buttons (FAB), botones elevados

### Personalización

Variables CSS personalizadas en `src/shared/styles/`:
- `variables.css`: Colores, tipografía, espaciado
- `base.css`: Estilos globales y resets

## 📊 Análisis de Bundle

Para analizar el tamaño del bundle y optimizaciones:

```bash
# Instalar plugin de análisis
pnpm add -D rollup-plugin-visualizer

# Ejecutar build con análisis
pnpm run build
```

Esto genera `stats.html` con visualización interactiva del bundle.

## 🐛 Debugging

### Sourcemaps

Los sourcemaps están habilitados en producción para debugging:

```javascript
// vite.config.js
export default {
  build: {
    sourcemap: true  // Genera .js.map y .css.map
  }
}
```

### DevTools

En desarrollo, usa las DevTools del navegador:
- **Console**: Ver logs y errores
- **Network**: Verificar carga de módulos
- **Sources**: Debugging con breakpoints

## 🚨 Solución de Problemas

### Puerto 5173 ocupado

Cambiar puerto en `vite.config.js`:

```javascript
export default {
  server: {
    port: 5174
  }
}
```

### Assets no se actualizan

1. Limpiar caché de Vite: `rm -rf node_modules/.vite`
2. Recompilar: `pnpm run build`
3. Reiniciar Django: `python manage.py runserver`

### ESLint errors en imports

Verificar `jsconfig.json` y ajustar paths si es necesario.

## 📚 Recursos

- **[Vite Documentation](https://vitejs.dev/)** - Guía oficial de Vite
- **[Materialize CSS](https://materializecss.com/)** - Componentes y ejemplos
- **[ESLint Rules](https://eslint.org/docs/rules/)** - Reglas de linting
- **[Prettier Options](https://prettier.io/docs/en/options.html)** - Opciones de formateo

## 🤝 Contribuir

Para contribuir al frontend:

1. Seguir [JavaScript Patterns](../../docs/JAVASCRIPT_PATTERNS.md)
2. Ejecutar `pnpm run lint:fix` antes de commit
3. Formatear código con `pnpm run format`
4. Testear en múltiples navegadores
5. Verificar build de producción con `pnpm run build`

Ver [CONTRIBUTING.md](../../docs/CONTRIBUTING.md) para guía completa.
