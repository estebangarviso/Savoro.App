# Copilot Instructions for Savoro.App

## Project Overview

Savoro.App is a modular restaurant management system built with Django (Python backend) and Materialize CSS (frontend). The architecture is inspired by NestJS, using a clear separation of concerns: **Controller → Service → Repository**. Each domain (e.g., dish, category, authentication) is implemented as a Django app under `modules/`.

## Key Architectural Patterns

- **Modular Structure:**
  - Each feature/domain is a Django app in `modules/` (e.g., `dish`, `category`, `authentication`).
  - Shared logic lives in `core/` (e.g., `core/base/services.py`, `core/base/repositories.py`).
- **Layered Approach:**
  - Controllers handle HTTP requests and delegate to services.
  - Services contain business logic and interact with repositories.
  - Repositories abstract data access (ORM queries, etc.).
- **Soft Delete:**
  - All models implement logical deletion (not physical). Check for custom model managers or mixins in `core/base/models.py`.
- **Localization:**
  - Chilean formats for dates, numbers, and currency. See `config/formats/es_CL.py`.
- **Type Safety:**
  - Extensive use of Python type hints. Linting via `pylint` is expected.

## Developer Workflows

- **Setup:**
  - Use `./scripts/setup.sh`, `make setup`, or `pnpm run setup` for initial environment setup (Python, JS, DB migrations, static files).
- **Development:**
  - Start dev server: `./scripts/start-dev.sh` (runs Django + Vite asset build).
  - Frontend assets: Built with Vite. Use `pnpm run build` or `pnpm run build:watch`.
- **Database:**
  - Migrations via `manage.py` or Makefile targets.
- **Superuser Creation:**
  - `pipenv run python manage.py createsuperuser` or `make superuser`.

## Conventions & Patterns

- **Naming:**
  - Use singular for models (`Dish`, `Category`), plural for querysets.
- **Permissions:**
  - Decorators in `core/decorators/` for access control.
- **Validation:**
  - Custom validators in `core/validators/`.
- **Mixins:**
  - Shared logic for filtering, pagination, etc. in `core/mixins/`.
- **Text Normalization:**
  - Accent-insensitive search via utilities in `core/utils/text.py`.

## Integration Points

- **Frontend:**
  - Materialize CSS, Vite for asset pipeline.
- **Backend:**
  - Django ORM, custom repository pattern.
- **Static Files:**
  - Collected via Django's `collectstatic`.

## Examples

- To add a new domain (e.g., `table`):
  1. Create a Django app in `modules/table/`.
  2. Implement `controller.py`, `service.py`, `repository.py`, and `models.py` following existing patterns.
  3. Register URLs in `modules/table/urls.py` and include in main `config/urls.py`.

## References

- Main config: `config/settings/`
- Core patterns: `core/base/`
- Scripts: `scripts/`
- Domain modules: `modules/`

---

_If any section is unclear or missing, please provide feedback for further refinement._
