#!/bin/bash

# Savoro App - Production Build Script
# Este script prepara la aplicación para producción

set -e

echo "🏭 Preparando Savoro App para producción..."
echo ""

# Colores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar que estamos en el entorno virtual
if ! pipenv --venv &> /dev/null; then
    echo -e "${RED}❌ Entorno virtual no encontrado${NC}"
    echo -e "${YELLOW}   Ejecuta: pipenv install${NC}"
    exit 1
fi

# Verificar node_modules
if [ ! -d "node_modules" ]; then
    echo -e "${RED}❌ node_modules no encontrado${NC}"
    echo -e "${YELLOW}   Ejecuta: pnpm install${NC}"
    exit 1
fi

# Limpiar build anterior dinámicamente
echo -e "${BLUE}🧹 Limpiando archivos de build anteriores...${NC}"


# Limpiar manifest y cache de Vite
rm -rf apps/frontend/staticfiles/.vite

# Limpiar JS y CSS generados por Vite en cada módulo
for module_dir in apps/frontend/staticfiles/*/; do
    module_name=$(basename "$module_dir")
    [ -d "apps/frontend/staticfiles/$module_name/js" ] && rm -rf "apps/frontend/staticfiles/$module_name/js"
    [ -d "apps/frontend/staticfiles/$module_name/css" ] && rm -rf "apps/frontend/staticfiles/$module_name/css"
done

# Limpiar shared si existe
[ -d "apps/frontend/staticfiles/shared/js" ] && rm -rf "apps/frontend/staticfiles/shared/js"
[ -d "apps/frontend/staticfiles/shared/css" ] && rm -rf "apps/frontend/staticfiles/shared/css"

# Limpiar chunks generados por Vite
[ -d "apps/frontend/staticfiles/js/chunks" ] && rm -rf "apps/frontend/staticfiles/js/chunks"

echo -e "${GREEN}✓ Limpieza completada${NC}"

# Compilar assets con Vite (producción)

echo -e "${BLUE}🔨 Compilando assets con Vite (modo producción)...${NC}"
cd apps/frontend
NODE_ENV=production pnpm run build
cd ../..

# Verificar que la compilación fue exitosa
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Error en la compilación de Vite${NC}"
    exit 1
fi

# Recopilar archivos estáticos de Django

echo -e "${BLUE}📁 Recopilando archivos estáticos de Django...${NC}"
pipenv run python apps/backend/manage.py collectstatic --noinput --clear

# Ejecutar migraciones

echo -e "${BLUE}🗄️  Aplicando migraciones de base de datos...${NC}"
pipenv run python apps/backend/manage.py migrate --noinput

echo ""
echo -e "${GREEN}✅ Build de producción completado exitosamente${NC}"
echo ""
echo -e "${YELLOW}📊 Resumen de archivos generados:${NC}"

echo -e "   - Archivos JavaScript con sourcemaps en apps/frontend/staticfiles/*/js/"
echo -e "   - Archivos CSS optimizados en apps/frontend/staticfiles/*/css/"
echo -e "   - Manifest de Vite en apps/frontend/staticfiles/.vite/manifest.json"
echo ""
echo -e "${BLUE}🚀 Para ejecutar en producción:${NC}"
echo -e "   pipenv run gunicorn config.wsgi:application --bind 0.0.0.0:8000"
echo ""
