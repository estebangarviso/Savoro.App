# Guía de Diseño y Estándares UI/UX
**Stack:** Penpot (Self-hosted) + RSuite + React / React Native

Este documento define las reglas visuales, la paleta de colores y las pruebas de calidad (QA de Diseño) necesarias para asegurar que nuestros wireframes sean funcionales y estéticos.

## 1. 🔡 Tipografía: Roboto

Hemos seleccionado **Roboto** como nuestra fuente corporativa.

### ¿Por qué Roboto?

* **Nativa en Android:** Al ser la fuente por defecto de Android, nuestra App en React Native se sentirá 100% nativa y fluida sin peso extra en el bundle.
* **Neutralidad:** Es una tipografía "Grotesca" geométrica que funciona perfecto con el estilo limpio de RSuite.
* **Versatilidad:** Posee una gran variedad de pesos (Thin a Black) que nos permiten crear jerarquías visuales claras.

### Implementación

* **En Penpot:** Si no aparece en el selector, subir los archivos `.ttf` desde Google Fonts a la configuración del equipo.
* **Pesos permitidos:**
  * Regular (400) - Texto cuerpo.
  * Medium (500) - Botones y Subtítulos.
  * Bold (700) - Encabezados importantes.


## 2. 🎨 Paleta de Colores (Sistema RSuite)

Para facilitar el desarrollo, utilizaremos una adaptación de la paleta por defecto de RSuite (Blue).

### Colores Primarios (Brand)

Usados para acciones principales, estados activos y destacados.

* 🔵 **Primary Main:** `#3498FF` (RSuite Blue base)
* 🔵 **Primary Hover:** `#2589F5` (Interacción)
* 🔵 **Primary Dark:** `#0060AA` (Textos sobre fondos claros)

### Colores Neutros (Grays)

Usados para texto, bordes y fondos.

* ⚫ **Text Primary:** `#272C36` (Casi negro - Títulos)
* ⚫ **Text Secondary:** `#575757` (Cuerpo de texto)
* ⚪ **Borders:** `#E5E5EA` (Divisiones sutiles)
* ⚪ **Background:** `#F7F7FA` (Fondos de pantalla app/web)

### Colores Semánticos (Feedback)

* 🟢 **Success:** `#58B15B` (Completado, Aprobado)
* 🔴 **Error:** `#F44336` (Fallos, Borrar, Alertas críticas)
* 🟠 **Warning:** `#FFB300` (Precaución, Pendiente)

> **Regla de Diseño:** No uses negro puro (`#000000`) ni gris por defecto. Usa siempre los códigos hexadecimales de arriba para mantener la elegancia.
s
## 3. 🧪 Pruebas Prácticas de UI/UX (Design QA)

Antes de pasar un diseño a desarrollo (Handoff), el wireframe debe aprobar estas 4 pruebas rápidas:

### A. La Prueba del Pulgar (The Thumb Zone) - *Solo Mobile*
* **Objetivo:** Verificar que la app sea usable con una mano.
* **Check:**
    * ¿Los botones de acción principal (CTA) están en el tercio inferior de la pantalla?
    * ¿El botón "Atrás" o el menú hamburguesa es accesible sin estirar demasiado el dedo?

### B. La Regla de los 44px (Touch Targets)
* **Objetivo:** Evitar la frustración del usuario al tocar botones pequeños ("Fat finger error").
* **Check:**
    * Ningún elemento interactivo (botón o icono clicable) debe medir menos de **44x44px** (o tener un padding transparente que llegue a ese tamaño).
    * En Penpot, asegúrate de que el contenedor del icono tenga ese tamaño mínimo.

### C. Prueba de Contraste (Accesibilidad)
* **Objetivo:** Asegurar que el texto se lea bien sobre el fondo.
* **Herramienta:** Usa el plugin de Penpot "Contrast Checker" o una web externa.
* **Check:**
    * Texto normal: Ratio mínimo de **4.5:1**.
    * Texto grande/negrita: Ratio mínimo de **3:1**.
    * *Ejemplo:* No poner texto gris claro sobre fondo blanco.

### D. The Squint Test (La prueba de entrecerrar los ojos)
* **Objetivo:** Validar la Jerarquía Visual.
* **Acción:** Aléjate de la pantalla y entrecierra los ojos hasta que todo se vea borroso.
* **Check:**
    * ¿Sigue destacando el botón más importante (Primary Button)?
    * ¿Se entiende cuál es el título y cuál es el contenido?
    * Si todo se ve como una mancha gris uniforme, falta contraste o jerarquía (tamaño/negrita).


## 4. 🧩 Sistema de Iconos: FontAwesome

* **Librería:** FontAwesome 6 (Versión Free).
* **Formato:** SVG Vectorial (a través de Penpot Libraries).
* **Consistencia:**
    * Todos los iconos deben tener el mismo estilo (Solid o Regular). No mezclar estilos en la misma pantalla.
    * Si el texto es gris, el icono debe ser gris (o Primary si es interactivo).


## 5. 🚀 Flujo de Trabajo y Buenas Prácticas

1.  **Mobile First:** Diseña primero la pantalla de React Native (360px ancho). Es más fácil escalar hacia Web que reducir desde Web.
2.  **Layouts Flex:** Usa siempre las herramientas de Flexbox de Penpot (`Gap`, `Align`, `Justify`). No posiciones elementos "a ojo".
3.  **Componentes:** Si un elemento se repite más de 2 veces (ej: una tarjeta de producto), conviértelo en Componente en Penpot.