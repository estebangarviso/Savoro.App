# Guía de Contribución - Savoro.App

## Flujo de Trabajo (Git Flow)

1. Fork el repositorio
2. Crear rama desde `develop` usando Git Flow:

   ```bash
   # Inicializar Git Flow (solo primera vez)
   git flow init
   
   # Crear feature branch
   git flow feature start amazing-feature
   
   # Crear hotfix branch (desde main)
   git flow hotfix start fix-critical-bug
   
   # Crear release branch
   git flow release start 1.0.0
   ```

3. Realizar commits con [Conventional Commits](https://www.conventionalcommits.org/):

   ```bash
   git commit -m "feat: add user authentication"
   git commit -m "fix: resolve login validation issue"
   git commit -m "docs: update installation guide"
   git commit -m "refactor: optimize database queries"
   git commit -m "style: format code with prettier"
   git commit -m "test: add unit tests for category service"
   git commit -m "chore: update dependencies"
   ```

4. Finalizar feature/hotfix/release:

   ```bash
   # Finalizar feature (merge a develop)
   git flow feature finish amazing-feature
   
   # Finalizar hotfix (merge a main y develop)
   git flow hotfix finish fix-critical-bug
   
   # Finalizar release (merge a main y develop, crear tag)
   git flow release finish 1.0.0
   ```

5. Push y abrir Pull Request con descripción clara

## Ramas Git Flow

| Rama        | Propósito                    | Se crea desde | Se fusiona a         |
| ----------- | ---------------------------- | ------------- | -------------------- |
| `main`      | Código en producción         | -             | -                    |
| `develop`   | Rama de desarrollo principal | `main`        | `main` (via release) |
| `feature/*` | Nuevas funcionalidades       | `develop`     | `develop`            |
| `release/*` | Preparación de release       | `develop`     | `main` + `develop`   |
| `hotfix/*`  | Correcciones críticas        | `main`        | `main` + `develop`   |

## Convención de Nombres

### Features

`feature/` + descripción en kebab-case
- `feature/add-reservation-system`
- `feature/dish-export-pdf`
- `feature/user-authentication`

### Hotfixes

`hotfix/` + descripción del bug
- `hotfix/login-validation-error`
- `hotfix/image-upload-crash`
- `hotfix/security-vulnerability`

### Releases

`release/` + versión semántica
- `release/1.0.0`
- `release/1.1.0`
- `release/2.0.0-beta`

## Tipos de Commits

| Tipo       | Descripción             | Ejemplo                               |
| ---------- | ----------------------- | ------------------------------------- |
| `feat`     | Nueva funcionalidad     | `feat: add dish export to PDF`        |
| `fix`      | Corrección de errores   | `fix: resolve image upload bug`       |
| `docs`     | Documentación           | `docs: update API documentation`      |
| `style`    | Formato de código       | `style: apply ESLint rules`           |
| `refactor` | Refactorización         | `refactor: simplify category service` |
| `test`     | Tests                   | `test: add integration tests`         |
| `chore`    | Tareas de mantenimiento | `chore: update django to 4.2.8`       |
| `perf`     | Mejoras de rendimiento  | `perf: optimize query performance`    |

## Estándares de Código

### Python

- Seguir PEP 8
- Usar type hints en funciones y métodos
- Documentar clases y funciones complejas con docstrings
- Ejecutar tests antes de hacer commit
- Usar nombres descriptivos en inglés para código, español para mensajes de usuario

**Herramientas de linting:**

```bash
# Linter principal (configurado para Django)
pipenv run pylint modules/ core/

# Formatear código con black
pipenv run black modules/ core/

# Ordenar imports con isort
pipenv run isort modules/ core/
```

### JavaScript

- Seguir configuración ESLint del proyecto
- Usar sintaxis ES2021+
- camelCase para variables y funciones
- PascalCase para clases
- NO contaminar el scope global (window)
- Usar Custom Events para comunicación template ↔ JS
- Documentar funciones con JSDoc

**Herramientas de linting:**

```bash
# Linter JavaScript
pnpm run lint

# Formatear con Prettier
pnpm run format

# Verificar antes de commit
pnpm run lint:fix
```

### CSS

- Usar clases BEM-like descriptivas
- Aprovechar CSS Variables definidas
- Mobile First approach
- Mantener especificidad baja
- No usar !important (excepto casos justificados)

### Templates Django

- Usar indentación consistente
- Comentar secciones complejas
- Evitar lógica compleja en templates
- Usar template tags personalizados para lógica reutilizable

**Herramientas de linting:**

```bash
# Linter para templates Django
pipenv run djlint modules/ shared/ --reformat
```

## Testing

### Tests de Backend

```python
# tests/test_dish_service.py
from django.test import TestCase
from modules.dish.service import DishService

class DishServiceTest(TestCase):
    def setUp(self):
        self.service = DishService()
    
    def test_create_dish_success(self):
        data = {"name": "Test Dish", "price": 10000}
        dish = self.service.create(data)
        self.assertEqual(dish.name, "Test Dish")
    
    def test_create_dish_duplicate_name(self):
        data = {"name": "Test Dish", "price": 10000}
        self.service.create(data)
        
        with self.assertRaises(BadRequestException):
            self.service.create(data)
```

**Ejecutar tests:**

```bash
# Todos los tests
pipenv run python manage.py test

# Tests específicos
pipenv run python manage.py test modules.dish.tests

# Con coverage
pipenv run coverage run manage.py test
pipenv run coverage report
```

### Tests de Frontend

Para JavaScript, considerar usar Jest o Vitest:

```javascript
// tests/messages.test.js
import { displayToast } from '@shared/js/messages.js';

describe('displayToast', () => {
  test('shows success toast', () => {
    displayToast('Success!', 'success');
    // Assert toast appears
  });
  
  test('shows error toast with longer duration', () => {
    displayToast('Error!', 'error');
    // Assert toast appears and duration is 5000ms
  });
});
```

## Checklist Pre-Commit

- [ ] Código formateado (Python: black + isort, JS: Prettier)
- [ ] Tests pasan exitosamente
- [ ] No hay errores de linting (pylint, eslint, djlint)
- [ ] Type hints correctos (pylint)
- [ ] Documentación actualizada si aplica
- [ ] Commit sigue Conventional Commits
- [ ] Sin archivos innecesarios (logs, cache, \__pycache__, node_modules)
- [ ] Migraciones creadas si hay cambios en modelos

## Checklist Pull Request

- [ ] Título descriptivo siguiendo convención de Git Flow
- [ ] Descripción clara del cambio con contexto
- [ ] Tests incluidos para nueva funcionalidad
- [ ] Screenshots/GIFs si hay cambios visuales
- [ ] Sin conflictos con rama base (develop/main)
- [ ] Code review solicitado
- [ ] Documentación actualizada (README, ARCHITECTURE, etc.)
- [ ] Migraciones incluidas y testeadas
