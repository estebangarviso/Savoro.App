# Guía de Diseño y Entorno de Desarrollo

**Proyecto:** App Multiplataforma (Web & Mobile)
**Stack:** Penpot (Self-hosted) + RSuite + React + FontAwesome

Este documento detalla cómo levantar el entorno de diseño local, los estándares visuales (Roboto + RSuite) y las pruebas de calidad UI/UX requeridas.

## ⚡ 1. Puesta en Marcha (Docker)

Para trabajar en los wireframes, necesitamos levantar nuestra instancia local de Penpot.

### Requisitos

* Docker y Docker Compose instalados.
* Archivo `docker-compose.yaml` en la raíz de este directorio.

### Comandos de Inicio

Abre tu terminal en la carpeta del proyecto y ejecuta:

```bash
# Levantar los contenedores en segundo plano
docker compose up -d
```

*(Nota: Si usas una versión antigua de Docker, usa `docker-compose up -d`)*

### Acceso

Una vez finalizado el arranque:

1. Abre tu navegador en: **<http://localhost:9001>**
2. Si es tu primera vez, crea una cuenta (no requiere verificación de email en entorno local).

## 2. 🔡 Tipografía: Roboto

Utilizaremos **Roboto** como fuente única para garantizar consistencia nativa en Android y neutralidad en Web.

* **Pesos Permitidos:**
  * `Regular (400)`: Texto general, párrafos.
  * `Medium (500)`: Botones, inputs, subtítulos.
  * `Bold (700)`: Títulos principales (H1, H2).
* **Configuración:** Si la fuente no aparece en Penpot, subir los archivos `.ttf` en *Team Settings \> Fonts*.

## 3. 🎨 Paleta de Colores (RSuite System)

Usamos una adaptación del sistema "RSuite Blue" para facilitar la implementación en código.

| Uso         | Color          | Hex       | Notas                             |
| :---------- | :------------- | :-------- | :-------------------------------- |
| **Primary** | RSuite Blue    | `#3498FF` | Botones, Links, Estados Activos.  |
| **Hover**   | Blue Hover     | `#2589F5` | Interacción al pasar el mouse.    |
| **Dark**    | Blue Dark      | `#0060AA` | Textos sobre fondos claros.       |
| **Text**    | Title Black    | `#272C36` | Encabezados (No usar negro puro). |
| **Text**    | Body Gray      | `#575757` | Párrafos y etiquetas secundarias. |
| **Bg**      | App Background | `#F7F7FA` | Fondo general de pantallas.       |
| **Status**  | Error Red      | `#F44336` | Alertas críticas.                 |

## 4. 🧪 Pruebas Prácticas de UI/UX (QA Checklist)

Antes de aprobar un diseño, debe superar estas 4 pruebas:

### ✅ A. La Prueba del Pulgar (Thumb Zone) - *Mobile*

Verifica que las zonas de interacción principales sean alcanzables con una mano.

* **OK:** Botones de acción (Guardar, Siguiente) en el tercio inferior.
* **OK:** Menús de navegación al alcance del pulgar.

### ✅ B. La Regla de los 44px

Evita el "error de dedo gordo".

* Ningún elemento táctil debe medir menos de **44x44px** (incluyendo padding transparente). Si el icono es pequeño, agranda su contenedor en Penpot.

### ✅ C. Contraste y Legibilidad

* Texto normal: Ratio mínimo **4.5:1** contra el fondo.
* No usar gris claro sobre fondo blanco. Usa el plugin de contraste de Penpot si tienes dudas.

### ✅ D. The Squint Test (Entrecerrar los ojos)

Aléjate y entrecierra los ojos hasta ver borroso:

* ¿Aún se distingue cuál es el botón principal (Primary)?
* ¿Se diferencia el título del contenido?
* *Si todo se ve gris plano, falta jerarquía (negritas o tamaño).*

## 5. 🧩 Iconografía

* **Librería:** **FontAwesome 6 (Free)**.
* **Formato:** Usar solo SVGs desde las *Penpot Shared Libraries*.
* **Estilo:** Mantener consistencia (no mezclar iconos rellenos con iconos de línea en la misma vista).

## 6. 🚀 Buenas Prácticas de Diseño

1. **Mobile First:** Diseña siempre el Artboard de **360x800** primero.
2. **Layouts Flex:** No agrupes formas. Usa la herramienta **Layout (Flex)** de Penpot para definir `Gap` y `Padding`. Esto genera el código CSS/React Native automáticamente.
3. **Nombres de Capas:** Nombra las capas como componentes de React (ej: `SubmitButton`, `HeaderContainer`) para agilizar el trabajo del desarrollador.
