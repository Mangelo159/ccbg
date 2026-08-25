function ccToggleUserMenu(event) {
    if (event) event.stopPropagation();
    var dropdown = document.getElementById('cc-user-dropdown');
    if (!dropdown) return;
    var abrir = !dropdown.classList.contains('is-open');
    dropdown.classList.toggle('is-open', abrir);
    var boton = dropdown.previousElementSibling;
    if (boton) boton.setAttribute('aria-expanded', abrir ? 'true' : 'false');
}

document.addEventListener('click', function (event) {
    var dropdown = document.getElementById('cc-user-dropdown');
    if (!dropdown || !dropdown.classList.contains('is-open')) return;
    if (dropdown.contains(event.target)) return;
    dropdown.classList.remove('is-open');
    var boton = dropdown.previousElementSibling;
    if (boton) boton.setAttribute('aria-expanded', 'false');
});

function ccOpenModal(type, data) {
    data = data || {};
    var dialog = document.getElementById('dialog-' + type);
    if (!dialog) return;

    var form = dialog.querySelector('form');
    if (form) {
        form.reset();
        Object.keys(data).forEach(function (key) {
            if (key === 'newTitle' || key === 'editTitle') return;
            var field = form.querySelector('[name="' + key + '"]');
            if (!field) return;
            if (field.type === 'checkbox') {
                field.checked = !!data[key];
            } else if (field.type !== 'file') {
                field.value = data[key] == null ? '' : data[key];
            }
        });
    }

    var title = dialog.querySelector('.cc-modal-title');
    if (title) title.textContent = data.id ? (data.editTitle || 'Editar') : (data.newTitle || 'Nuevo');

    dialog.showModal();
}

function ccCloseModal(type) {
    var dialog = document.getElementById('dialog-' + type);
    if (dialog) dialog.close();
}

/**
 * Buscador local de un módulo (Empresa/Barrio/Claro): filtra en vivo los
 * elementos con `data-cc-buscar` dentro de cada contenedor de resultados
 * (`.cc-module-section .cc-table tbody` para tablas, `.cc-recurso-grid` para
 * cards) según el texto acumulado en ese atributo. Se autoinicializa si
 * encuentra el input #cc-modulo-buscador, sin necesitar script por plantilla.
 */
document.addEventListener('DOMContentLoaded', function () {
    var input = document.getElementById('cc-modulo-buscador');
    if (!input) return;

    var contenedores = document.querySelectorAll('.cc-module-section .cc-table tbody, .cc-module-section .cc-recurso-grid');

    contenedores.forEach(function (contenedor) {
        var items = contenedor.querySelectorAll('[data-cc-buscar]');
        if (items.length === 0) return;

        var esTabla = contenedor.tagName === 'TBODY';
        var vacio;
        if (esTabla) {
            var tabla = contenedor.closest('table');
            var columnas = tabla ? tabla.querySelectorAll('thead th').length : 1;
            vacio = document.createElement('tr');
            var celda = document.createElement('td');
            celda.colSpan = columnas;
            celda.className = 'cc-table-empty';
            celda.textContent = 'Sin resultados para tu búsqueda.';
            vacio.appendChild(celda);
        } else {
            vacio = document.createElement('div');
            vacio.className = 'cc-table-empty';
            vacio.textContent = 'Sin resultados para tu búsqueda.';
        }
        vacio.classList.add('cc-table-search-empty');
        vacio.style.display = 'none';
        contenedor.appendChild(vacio);
    });

    input.addEventListener('input', function () {
        var termino = input.value.trim().toLowerCase();

        contenedores.forEach(function (contenedor) {
            var items = contenedor.querySelectorAll('[data-cc-buscar]');
            if (items.length === 0) return;

            var visibles = 0;
            items.forEach(function (item) {
                var coincide = termino === '' || item.getAttribute('data-cc-buscar').toLowerCase().indexOf(termino) !== -1;
                item.style.display = coincide ? '' : 'none';
                if (coincide) visibles++;
            });

            var vacio = contenedor.querySelector('.cc-table-search-empty');
            if (vacio) vacio.style.display = (termino !== '' && visibles === 0) ? '' : 'none';
        });
    });
});

var CC_TOKEN_RE = /\{\{\s*([A-Za-z0-9_]+)\s*\}\}/g;

function ccTokensFromText(text) {
    var tokens = [];
    var seen = {};
    var match;
    CC_TOKEN_RE.lastIndex = 0;
    while ((match = CC_TOKEN_RE.exec(text || '')) !== null) {
        var key = match[1].toUpperCase();
        if (!seen[key]) {
            seen[key] = true;
            tokens.push(key);
        }
    }
    return tokens;
}

function ccFillTemplate(text, values) {
    return (text || '').replace(CC_TOKEN_RE, function (match, token) {
        var key = token.toUpperCase();
        return Object.prototype.hasOwnProperty.call(values, key) ? values[key] : match;
    });
}

/**
 * Abre el modal "Usar plantilla": detecta los {{TOKEN}} presentes en `data.campos`
 * (un objeto { nombreDeSalida: textoPlantilla }), genera un input por token único
 * y actualiza la salida en vivo. No guarda nada ni modifica la plantilla original.
 */
function ccOpenUsarModal(type, data) {
    data = data || {};
    var dialog = document.getElementById('dialog-' + type);
    if (!dialog) return;

    var campos = data.campos || {};
    var combinado = Object.keys(campos).map(function (k) { return campos[k]; }).join('\n');
    var tokens = ccTokensFromText(combinado);
    var valores = {};

    var contenedor = dialog.querySelector('.cc-usar-campos');
    contenedor.innerHTML = '';

    function actualizarSalida() {
        Object.keys(campos).forEach(function (key) {
            var salida = dialog.querySelector('[data-salida="' + key + '"]');
            if (salida) salida.textContent = ccFillTemplate(campos[key], valores);
        });
    }

    if (tokens.length === 0) {
        var vacio = document.createElement('p');
        vacio.className = 'cc-modal-hint';
        vacio.textContent = 'Esta plantilla no tiene variables. Copia el texto directamente.';
        contenedor.appendChild(vacio);
    } else {
        tokens.forEach(function (token) {
            valores[token] = '';
            var wrap = document.createElement('div');
            wrap.className = 'cc-usar-campo';
            var label = document.createElement('label');
            label.className = 'cc-login-label';
            label.textContent = token;
            var input = document.createElement('input');
            input.type = 'text';
            input.className = 'cc-login-input';
            input.addEventListener('input', function () {
                valores[token] = input.value;
                actualizarSalida();
            });
            wrap.appendChild(label);
            wrap.appendChild(input);
            contenedor.appendChild(wrap);
        });
    }

    actualizarSalida();

    var title = dialog.querySelector('.cc-modal-title');
    if (title) title.textContent = data.title || 'Usar plantilla';

    dialog.showModal();
}

function ccCopiarSalida(type) {
    var dialog = document.getElementById('dialog-' + type);
    if (!dialog) return;
    var partes = [];
    dialog.querySelectorAll('[data-salida]').forEach(function (el) {
        partes.push(el.textContent);
    });
    var texto = partes.join('\n\n');
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(texto);
    }
}

var CC_EXT_IMAGEN = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp', 'svg'];

function ccTipoArchivo(url) {
    if (!url) return 'ninguno';
    var limpio = url.split('?')[0].split('#')[0];
    var partes = limpio.split('.');
    var ext = partes.length > 1 ? partes.pop().toLowerCase() : '';
    if (ext === 'pdf') return 'pdf';
    if (CC_EXT_IMAGEN.indexOf(ext) !== -1) return 'imagen';
    return 'otro';
}

/**
 * Abre la vista previa grande de un Documento. PDF e imágenes se renderizan
 * dentro del modal (el PDF usa el visor nativo del navegador, con sus propios
 * controles de página/zoom). Otros tipos muestran un aviso + enlace externo.
 */
function ccOpenPreview(data) {
    data = data || {};
    var dialog = document.getElementById('dialog-preview');
    if (!dialog) return;

    var visor = dialog.querySelector('.cc-preview-visor');
    visor.innerHTML = '';
    var tipo = ccTipoArchivo(data.url);

    if (tipo === 'pdf') {
        var iframe = document.createElement('iframe');
        iframe.src = data.url;
        iframe.className = 'cc-preview-frame';
        visor.appendChild(iframe);
    } else if (tipo === 'imagen') {
        var img = document.createElement('img');
        img.src = data.url;
        img.alt = data.nombre || '';
        img.className = 'cc-preview-image';
        visor.appendChild(img);
    } else {
        var aviso = document.createElement('p');
        aviso.className = 'cc-preview-fallback';
        aviso.textContent = 'Este tipo de archivo no se puede previsualizar aquí.';
        visor.appendChild(aviso);
    }

    var enlace = dialog.querySelector('.cc-preview-open');
    if (enlace) enlace.href = data.url || '#';

    var title = dialog.querySelector('.cc-modal-title');
    if (title) title.textContent = data.nombre || 'Vista previa';

    dialog.showModal();
}

function ccClosePreview() {
    var dialog = document.getElementById('dialog-preview');
    if (!dialog) return;
    dialog.close();
    dialog.querySelector('.cc-preview-visor').innerHTML = '';
}
