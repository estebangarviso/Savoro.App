.PHONY: help setup dev prod build clean install migrate superuser

# Variables
PYTHON := pipenv run python
PNPM := pnpm

help: ## Mostrar esta ayuda
	@echo "Savoro App - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""

setup: ## Configuración inicial completa del proyecto
	@echo "⚠️  Configurando proyecto..."
	@./scripts/setup.sh

dev: ## Iniciar servidor de desarrollo
	@echo "🚀 Iniciando desarrollo..."
	@./scripts/start-dev.sh

prod: ## Build de producción completo
	@echo "🏭 Generando build de producción..."
	@./scripts/build-prod.sh

build: ## Compilar assets con Vite
	@echo "🔨 Compilando assets..."
	@$(PNPM) run build
	@$(PYTHON) manage.py collectstatic --noinput

clean: ## Limpiar archivos generados
	@echo "🧹 Limpiando archivos..."
	@rm -rf staticfiles/.vite
	@find modules -type d -name "static" 2>/dev/null | while read -r static_dir; do \
		module_name=$$(basename $$(dirname "$$static_dir")); \
		rm -rf "staticfiles/$$module_name/js" "staticfiles/$$module_name/css" 2>/dev/null || true; \
	done
	@rm -rf staticfiles/shared/js staticfiles/shared/css 2>/dev/null || true
	@rm -rf staticfiles/js/chunks 2>/dev/null || true
	@rm -rf node_modules/.vite 2>/dev/null || true
	@rm -rf staticfiles/**/*.css staticfiles/**/*.js 2>/dev/null || true
	@echo "✅ Limpieza completada"

install: ## Instalar dependencias
	@echo "📦 Instalando dependencias..."
	@pipenv install --dev
	@$(PNPM) install

migrate: ## Ejecutar migraciones de base de datos
	@echo "🗄️  Ejecutando migraciones..."
	@$(PYTHON) manage.py migrate

superuser: ## Crear superusuario
	@echo "👤 Creando superusuario..."
	@$(PYTHON) manage.py createsuperuser

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	@$(PYTHON) manage.py test

lint: ## Verificar código con linters
	@echo "🔍 Verificando código..."
	@$(PNPM) run lint
	@pipenv run pylint **/*.py || true
	@pipenv run black --check **/*.py || true
	@pipenv run isort --check-only **/*.py || true

lint-fix: ## Corregir código con linters
	@echo "🔧 Corrigiendo código..."
	@pipenv run pylint **/*.py || true
	@pipenv run black **/*.py
	@pipenv run isort **/*.py

format: ## Formatear código
	@echo "✨ Formateando código..."
	@$(PNPM) run format

watch: ## Modo desarrollo con recarga automática (Vite)
	@echo "👁️  Iniciando Vite en modo watch..."
	@$(PNPM) run build:watch
