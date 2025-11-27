#!/bin/bash

# Savoro App - Initial Setup Script
# Este script configura el proyecto por primera vez

set -e

echo "⚙️  Configurando Savoro App por primera vez..."
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python 3 no encontrado. Instala Python 3.10-3.13${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python encontrado: $(python3 --version)${NC}"

# Verificar pipenv
if ! command -v pipenv &> /dev/null; then
    echo -e "${YELLOW}⚠️  pipenv no encontrado. Instalando...${NC}"
    pip3 install pipenv
fi

echo -e "${GREEN}✓ pipenv encontrado${NC}"

# Verificar pnpm
if ! command -v pnpm &> /dev/null; then
    echo -e "${YELLOW}⚠️  pnpm no encontrado. Instalando...${NC}"
    npm install -g pnpm
fi

echo -e "${GREEN}✓ pnpm encontrado${NC}"
echo ""

# Instalar dependencias de Python
echo -e "${BLUE}📦 Instalando dependencias de Python...${NC}"
cd apps/backend
pipenv install
cd ../..

# Instalar dependencias de Node
echo -e "${BLUE}📦 Instalando dependencias de JavaScript...${NC}"
cd apps/frontend
pnpm install
cd ../..

# Crear base de datos y ejecutar migraciones
echo -e "${BLUE}🗄️  Configurando base de datos...${NC}"
pipenv run python apps/backend/manage.py migrate

# Compilar assets iniciales
echo -e "${BLUE}🔨 Compilando assets con Vite...${NC}"
cd apps/frontend
pnpm run build
cd ../..

# Recopilar archivos estáticos
echo -e "${BLUE}📁 Recopilando archivos estáticos...${NC}"
pipenv run python apps/backend/manage.py collectstatic --noinput

echo ""
echo -e "${GREEN}✅ Configuración completada exitosamente${NC}"
echo ""
echo -e "${YELLOW}🎯 Próximos pasos:${NC}"
echo -e "   1. Crear superusuario: ${BLUE}pipenv run python apps/backend/manage.py createsuperuser${NC}"
echo -e "   2. Iniciar desarrollo: ${BLUE}./scripts/start-dev.sh${NC}"
echo -e "   3. O usar: ${BLUE}cd apps/frontend && pnpm run dev${NC}"
echo ""
