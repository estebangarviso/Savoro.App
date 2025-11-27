.PHONY: help setup dev prod build clean install migrate superuser

# Variables
PYTHON := pipenv run python apps/backend/manage.py
PNPM := cd apps/frontend && pnpm

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
	@make clean
	@./scripts/start-dev.sh

prod: ## Build de producción completo
	@echo "🏭 Generando build de producción..."
	@./scripts/build-prod.sh

build: ## Compilar assets con Vite
	@echo "🔨 Compilando assets..."
	@cd apps/frontend && pnpm run build

clean: ## Limpiar archivos generados
	@echo "🧹 Limpiando archivos..."
	@if [ ! -d "apps/frontend/staticfiles" ]; then \
		echo "⚠️  El directorio apps/frontend/staticfiles no existe. Saltando limpieza."; \
		exit 0; \
	else \
		echo "🗑️  Eliminando archivos generados por Vite..." ; \
		rm -rf apps/frontend/staticfiles/.vite ; \
		rm -rf apps/frontend/staticfiles/.vite-manifest.json ; \
		rm -rf apps/frontend/staticfiles/manifest.json ; \
		rm -rf apps/frontend/staticfiles/vendor ; \
		find apps/frontend/staticfiles -type f \( -name "*.js" -o -name "*.css" \) -delete ; \
		find apps/frontend/staticfiles -type d -name "chunks" -exec rm -rf {} + 2>/dev/null || true ; \
		rm -rf apps/frontend/node_modules/.vite ; \
		echo "✅ Limpieza completada" ; \
	fi

install: ## Instalar dependencias
	@echo "📦 Instalando dependencias..."
	@cd apps/backend && pipenv install --dev
	@cd apps/frontend && pnpm install

migrate: ## Ejecutar migraciones de base de datos
	@echo "🗄️  Ejecutando migraciones..."
	@pipenv run python apps/backend/manage.py migrate

superuser: ## Crear superusuario
	@echo "👤 Creando superusuario..."
	@pipenv run python apps/backend/manage.py createsuperuser

test: ## Ejecutar tests
	@echo "🧪 Ejecutando tests..."
	@pipenv run python apps/backend/manage.py test

lint: ## Verificar código con linters
	@echo "🔍 Verificando código..."
	@cd apps/frontend && pnpm run lint
	@cd apps/backend && pipenv run pylint **/*.py || true
	@cd apps/backend && pipenv run black --check **/*.py || true
	@cd apps/backend && pipenv run isort --check-only **/*.py || true

lint-fix: ## Corregir código con linters
	@echo "🔧 Corrigiendo código..."
	@cd apps/backend && pipenv run pylint **/*.py || true
	@cd apps/backend && pipenv run black **/*.py
	@cd apps/backend && pipenv run isort **/*.py

format: ## Formatear código
	@echo "✨ Formateando código..."
	@cd apps/frontend && pnpm run format

watch: ## Modo desarrollo con recarga automática (Vite)
	@echo "👁️  Iniciando Vite en modo watch..."
	@cd apps/frontend && pnpm run build:watch

hmr: ## Modo desarrollo con Hot Module Replacement (HMR)
	@echo "🔥 Iniciando Vite con HMR..."
	@cd apps/frontend && pnpm run dev
