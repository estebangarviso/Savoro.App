#!/bin/bash

# Savoro App - Development Start Script
# Este script inicia Vite y Django en paralelo para desarrollo

set -e

echo "🚀 Iniciando Savoro App en modo desarrollo..."
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar que estamos en el entorno virtual de pipenv
if ! pipenv --venv &> /dev/null; then
    echo -e "${YELLOW}⚠️  Entorno virtual no detectado. Creando...${NC}"
    pipenv install
fi

# Activar entorno virtual
echo -e "${BLUE}📦 Activando entorno virtual de Python...${NC}"
export PIPENV_VERBOSITY=-1

# Verificar que node_modules existe
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules no encontrado. Instalando dependencias...${NC}"
    pnpm install
fi

echo ""
echo -e "${GREEN}✅ Compilación completada${NC}"
echo ""
echo -e "${BLUE}🌐 Iniciando servidor Django...${NC}"
echo -e "${YELLOW}   Accede a: http://localhost:8000${NC}"
echo ""
echo -e "${YELLOW}💡 Ahora ejecuta 'pnpm run dev:frontend' en JavaScript Debug Terminal${NC}"
echo ""

# Iniciar Django
pipenv run python apps/backend/manage.py runserver
