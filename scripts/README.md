# Scripts de Automatización - Savoro.App

Esta carpeta contiene scripts de shell para automatizar tareas comunes de desarrollo y producción.

## 📜 Scripts Disponibles

### `setup.sh`
**Configuración inicial completa del proyecto**

Ejecuta automáticamente:
- ✅ Verificación de Python 3.10-3.13
- ✅ Instalación de pipenv (si no existe)
- ✅ Instalación de pnpm (si no existe)
- ✅ Instalación de dependencias Python (`pipenv install`)
- ✅ Instalación de dependencias JavaScript (`pnpm install`)
- ✅ Migraciones de base de datos (`migrate`)
- ✅ Compilación inicial de assets con Vite
- ✅ Recopilación de archivos estáticos

**Uso:**
```bash
./scripts/setup.sh
```

---

### `start-dev.sh`
**Iniciar servidor de desarrollo**

Ejecuta automáticamente:
- ✅ Verificación de entorno virtual pipenv
- ✅ Verificación de node_modules
- ✅ Compilación de assets con Vite (producción)
- ✅ Recopilación de archivos estáticos (collectstatic --clear)
- ✅ Inicio del servidor Django en http://localhost:8000

**Uso:**
```bash
./scripts/start-dev.sh
```

**💡 Tip:** Para desarrollo con Hot Module Replacement (HMR), ejecuta `pnpm run dev` en otra terminal.

---

### `build-prod.sh`
**Build de producción completo**

Ejecuta automáticamente:
- ✅ Verificación de entorno virtual y dependencias
- ✅ **Limpieza dinámica** de builds anteriores (detecta módulos automáticamente)
- ✅ Compilación optimizada con Vite (NODE_ENV=production)
- ✅ Recopilación de archivos estáticos (collectstatic --clear)
- ✅ Aplicación de migraciones de base de datos
- ✅ Generación de sourcemaps para debugging

**Uso:**
```bash
./scripts/build-prod.sh
```

**Características destacadas:**
- 🔄 **Limpieza dinámica**: Escanea `modules/` y `shared/` automáticamente
- 📦 **No requiere actualización manual**: Nuevos módulos se detectan automáticamente
- ⚡ **Optimización**: Minificación, tree-shaking y code splitting
- 🗺️ **Sourcemaps**: `.js.map` generados para debugging en producción

---

## 🔧 Características Técnicas

### Limpieza Dinámica
Los scripts usan escaneo de directorios para detectar módulos automáticamente:

```bash
# Escanea todos los módulos en modules/
for module_dir in modules/*/; do
    module_name=$(basename "$module_dir")
    # Limpia JS y CSS de este módulo
    rm -rf "staticfiles/$module_name/js"
    rm -rf "staticfiles/$module_name/css"
done

# Limpia shared si existe
[ -d "shared/static" ] && rm -rf "staticfiles/shared/{js,css}"
```

**Ventajas:**
- ✅ No necesitas editar scripts al crear nuevos módulos
- ✅ Solo limpia lo que existe (no genera errores)
- ✅ Mantiene otros archivos estáticos intactos

### Códigos de Color
Los scripts usan códigos ANSI para mejor legibilidad:
- 🟢 Verde: Operaciones exitosas
- 🔵 Azul: Acciones en progreso
- 🟡 Amarillo: Advertencias y tips
- 🔴 Rojo: Errores críticos

### Manejo de Errores
Todos los scripts usan `set -e` para detener ejecución ante errores y verifican:
- Existencia de entornos virtuales
- Disponibilidad de dependencias
- Éxito de compilaciones

---

## 🚀 Workflows Recomendados

### Primer Setup
```bash
./scripts/setup.sh
pipenv run python manage.py createsuperuser
./scripts/start-dev.sh
```

### Desarrollo Diario
```bash
# Terminal 1: Django con assets compilados
./scripts/start-dev.sh

# Terminal 2 (opcional): Vite con HMR
pnpm run dev
```

### Deploy a Producción
```bash
./scripts/build-prod.sh
# Luego ejecuta tu servidor WSGI (gunicorn, uwsgi, etc.)
```

---

## ⚙️ Alternativas

Estos scripts también se pueden ejecutar mediante:

**Makefile:**
```bash
make setup    # ./scripts/setup.sh
make dev      # ./scripts/start-dev.sh
make prod     # ./scripts/build-prod.sh
```

**npm:**
```bash
pnpm run setup      # Similar a setup.sh
pnpm run start:dev  # Similar a start-dev.sh
pnpm run start:prod # Similar a build-prod.sh
```

Elige el método que prefieras. Ver [COMMANDS.md](../docs/COMMANDS.md) para más detalles.
