# Custome Care — Sistema de Diseño

Sistema de diseño del portal interno **Custome Care** (centralización de información de Banca Empresa, Banco del Barrio, Claro, Contactos y KMD).
Base normativa: variante **2a** — sidebar colapsado con iconos, header minimal con breadcrumb, home centrado en el buscador global.

Uso: interno del banco. Stack objetivo: Django templates.

---

## 1. Color

| Token | Valor | Uso |
|---|---|---|
| `--cc-navy` | `#160f41` | Color de marca. Sidebar activo, títulos, avatares, botones primarios oscuros, texto principal. |
| `--cc-magenta` | `#d2006e` | Acento. Un solo acento por pantalla: acción principal, estado activo, alerta, enlace. |
| `--cc-gray` | `#f9fafb` | Fondo de sidebar, cabeceras de tabla, superficies secundarias. |
| `--cc-white` | `#ffffff` | Fondo de contenido, tarjetas, header, footer. |

Neutros derivados (no son colores nuevos: son navy desaturado, permitidos solo en estos valores):

| Token | Valor | Uso |
|---|---|---|
| `--cc-border` | `#e7e5ec` | Bordes de header, footer, tarjetas, tablas. |
| `--cc-border-soft` | `#eceaf0` | Bordes internos y separadores del home. |
| `--cc-row` | `#f0eef4` | Separador de filas de tabla, fondo de monograma inactivo. |
| `--cc-text` | `#160f41` | Texto principal. |
| `--cc-text-2` | `#77748a` | Texto secundario, descripciones. |
| `--cc-text-3` | `#9b98a8` | Texto terciario, placeholders, metadatos. |
| `--cc-text-4` | `#a5a2b0` | Etiquetas de sección, contadores. |

### Reglas de color
1. **Máximo dos fondos por pantalla**: blanco para el contenido, `#f9fafb` para sidebar/cabeceras. Nada más.
2. **El magenta no se usa como fondo grande.** Solo en: botón primario del buscador, monograma del módulo activo, badges de aviso, enlaces y microtexto de acción (`Entrar →`, `Abrir`).
3. **Una sola acción magenta visible por vista.** Si hay dos, la secundaria pasa a navy o a texto plano.
4. Nunca degradados de color. El único gradiente permitido es el del hero del home: `linear-gradient(180deg,#f9fafb 0%,#ffffff 100%)`.
5. Nunca sombras de color. Sombras solo en navy transparente: `0 1px 2px rgba(22,15,65,.04)`, `0 8px 24px rgba(22,15,65,.09)`.
6. Sin semáforo de color inventado. Un dato que requiere atención se marca en magenta; el resto en navy.

---

## 2. Tipografía

Dos familias, sin excepciones.

- **Montserrat** — títulos, nombres de módulo, cifras. Pesos 600 / 700 / 800.
- **IBM Plex Sans** — interfaz, texto corrido, datos, tablas, formularios. Pesos 400 / 500 / 600.

```html
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
```

### Escala

| Rol | Familia / peso | Tamaño | Notas |
|---|---|---|---|
| H1 hero del home | Montserrat 800 | 30 px | `letter-spacing:-.7px`, máx. 600 px de ancho, `text-wrap:pretty` |
| Título de página | Montserrat 700 | 19–25 px | `letter-spacing:-.2px` |
| Título de sección | Montserrat 700 | 15 px | |
| Nombre de módulo (tarjeta) | Montserrat 700 | 13.5 px | `line-height:1.25` |
| Cifra / KPI | Montserrat 700 | 24 px | |
| Marca "Custome Care" | Montserrat 700 | 14 px | |
| Monograma | Montserrat 700–800 | 10–13 px | |
| Etiqueta de sección | IBM Plex 600 | 9.5–10 px | `letter-spacing:1.2–1.6px`, MAYÚSCULAS |
| Navegación / breadcrumb | IBM Plex 600 | 12 px | |
| Cuerpo | IBM Plex 400 | 12.5–14 px | |
| Descripción de tarjeta | IBM Plex 400 | 11–12 px | `line-height:1.45` |
| Dato de tabla | IBM Plex 400–500 | 12 px | |
| Cabecera de tabla | IBM Plex 600 | 10 px | `letter-spacing:.7px`, MAYÚSCULAS |
| Metadato / footer | IBM Plex 400 | 11–11.5 px | |
| Etiqueta de icono en sidebar | IBM Plex 400–500 | 8.5 px | único tamaño bajo 11 px permitido |

### Reglas de tipografía
1. Montserrat **nunca** en párrafos ni celdas de tabla. IBM Plex **nunca** en H1 ni en cifras grandes.
2. MAYÚSCULAS solo con `letter-spacing` y en tamaños de 9.5–10 px (etiquetas y cabeceras). Jamás en títulos.
3. Mínimo 11 px, salvo la etiqueta del sidebar colapsado (8.5 px).
4. Sin cursivas, sin subrayados (excepto `:hover` de enlaces en texto), sin `text-shadow`.

---

## 3. Espaciado y forma

Escala base de 4 px: `4 · 6 · 9 · 12 · 16 · 20 · 26 · 30 · 40 · 46`.

| Radio | Uso |
|---|---|
| 6–8 px | Badges, chips, monogramas pequeños, botones de icono |
| 9–10 px | Botones, tarjetas de KPI, ítems de sidebar |
| 12–14 px | Tarjetas de contenido, barra del buscador |
| 50% | Avatares |

Densidad: **equilibrada**. Padding de contenido 26–30 px, de tarjeta 14–18 px, de fila de tabla 13 px vertical.

Bordes: 1 px sólido siempre. Los únicos bordes gruesos permitidos son el `2px` del buscador principal (navy) y el `3px` superior de las tarjetas de módulo.

---

## 4. Layout maestro (`base.html`)

```
┌────────┬────────────────────────────────────────┐
│        │ header  60 px                          │
│ side   ├────────────────────────────────────────┤
│ bar    │                                        │
│ 82 px  │ {% block content %}                    │
│        │                                        │
│        ├────────────────────────────────────────┤
│        │ footer  42 px                          │
└────────┴────────────────────────────────────────┘
```

- El sidebar es de **altura completa**; el header vive dentro de la columna de contenido (no cruza el sidebar).
- Header y footer son fijos en altura; solo el contenido crece.
- Ancho de referencia del diseño: 1180 px. Contenido sin límite máximo; el hero del buscador se limita a 640 px y se centra.

Bloques de plantilla obligatorios: `title`, `breadcrumb`, `content`, `extra_css`, `extra_js`.

### Sidebar
- Ancho colapsado **82 px**. Marca (monograma `CC` navy, 32 px) arriba, separada 14 px.
- Cinco ítems, siempre en este orden y hardcodeados: **Banca Empresa · Banco del Barrio · Claro · Contactos · KMD**.
- Cada ítem: monograma de 28 px + etiqueta corta de 8.5 px, dentro de un bloque de 64 px con radio 10 px.
- Activo: bloque con fondo navy, monograma magenta, etiqueta blanca. Inactivo: sin fondo, monograma `#f0eef4` con texto navy, etiqueta `#77748a`.
- Al pie: botón de expandir (flecha) y avatar del usuario.
- Área de clic mínima 44 px de alto por ítem.

### Header
- Izquierda: breadcrumb `Sección / Subsección` (activo en navy 600, resto en `#9b98a8`).
- Derecha: fecha y hora, separador de 1 px, campana con punto magenta, avatar navy de 30 px.
- Sin buscador en el header. **El buscador vive en el home.**

### Footer
- Fondo blanco, borde superior, 42 px. Izquierda: `Custome Care · Uso interno del banco`. Derecha: versión y extensión de soporte.

---

## 5. Home (`home.html`)

Dos zonas, en este orden:

**1. Hero de búsqueda global** — fondo con el gradiente permitido, centrado, padding `46px 30px 40px`, borde inferior.
- Etiqueta `CENTRO DE INFORMACIÓN INTERNA` en magenta.
- H1 de una sola línea de mensaje.
- Barra de búsqueda: máx. 640 px, borde navy de 2 px, radio 14 px, lupa a la izquierda, placeholder `Cliente, RUC, cédula, número de caso o convenio…`, botón magenta `Buscar`.
- Debajo: búsquedas recientes como texto plano (máx. 3), no como chips.

**2. Accesos rápidos** — encabezado `Accesos rápidos` + enlace magenta a la derecha; grid de **5 columnas iguales**, gap de 12 px.
- Tarjeta: borde superior de 3 px (magenta si es el módulo del usuario, navy el resto), sin radio arriba, radio 10 px abajo.
- Contenido: nombre del módulo (Montserrat 700), descripción de una línea, contador de registros al pie.

Reglas del home:
1. El buscador es el primer elemento del contenido. Nada por encima de él.
2. Sin KPIs, gráficas ni tablas en el home. Esos bloques pertenecen a las vistas de módulo.
3. Las cinco tarjetas siempre visibles y del mismo tamaño. Si se agrega un módulo, el grid pasa a 6 columnas o a dos filas de 3, nunca tarjetas de tamaños distintos.

---

## 6. Componentes

**Botón primario** — fondo magenta, texto blanco IBM Plex 600 12.5 px, padding `11px 22px`, radio 10 px.
**Botón secundario** — fondo navy, mismas medidas. Usar solo si no compite con un primario magenta.
**Botón terciario** — sin fondo, texto navy 600, borde `#e7e5ec`.
**Badge de aviso** — texto magenta sobre `rgba(210,0,110,.08)`, radio 20 px, padding `5px 11px`.
**Chip de filtro** — borde `#e7e5ec`, radio 20 px; seleccionado: borde magenta y texto navy (no fondo lleno).
**Monograma de módulo** — dos letras: `BE · BB · CL · CT · KM`. Es el sistema de iconografía del producto; sustituye a cualquier librería de iconos para módulos.
**Tarjeta de KPI** (vistas de módulo) — etiqueta MAYÚSCULAS 10.5 px `#9b98a8` + cifra Montserrat 700 24 px. Magenta solo si el dato exige acción.
**Tabla** — cabecera `#f9fafb`, filas separadas por `#f0eef4`, números alineados a la derecha, última columna con acción magenta `Abrir`.

### Iconografía
Iconos de línea de 14–18 px, `stroke-width:2`, `stroke-linecap:round`, en `currentColor` o `#77748a`. Solo los estrictamente funcionales: lupa, campana, flecha de expandir. Sin iconos decorativos, sin emojis, sin ilustraciones.

---

## 7. Prohibiciones

- No agregar colores fuera de la tabla de la sección 1.
- No usar una tercera familia tipográfica.
- No poner buscador en el header ni duplicarlo en el home.
- No degradados de marca, sombras de color, bordes redondeados mayores a 14 px ni tarjetas con acento en el borde izquierdo.
- No emojis ni ilustraciones generadas.
- No reordenar ni renombrar los cinco módulos.
- No mezclar tarjetas y tabla densa en la misma vista sin jerarquía clara (KPIs arriba, tabla abajo).

---

## 8. Implementación en Django

```
templates/
  base.html          # sidebar + header + footer + bloques
  home.html          # extends base.html
static/
  css/cc.css         # variables de la sección 1 + utilidades
```

- Definir los tokens de color como variables CSS en `:root` dentro de `cc.css` y consumirlos con `var(--cc-navy)`, etc. No repetir hexadecimales en las plantillas.
- Los cinco módulos van hardcodeados en `base.html` (no vienen de la base de datos), con la clase `is-active` aplicada según una variable de contexto `modulo_activo`.
- Nombres de bloque: `{% block title %}`, `{% block breadcrumb %}`, `{% block content %}`, `{% block extra_css %}`, `{% block extra_js %}`.
- Todo asset por `{% static %}`.
