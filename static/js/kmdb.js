/**
 * Chat de KMDB: mantiene el historial de la conversación en memoria (formato
 * de mensajes de la API de Anthropic) y lo reenvía en cada pregunta para que
 * el asistente tenga contexto de los turnos previos. El historial no se
 * persiste; se pierde al recargar la página.
 */
document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('cc-kmdb-form');
    if (!form) return;

    var lista = document.getElementById('cc-kmdb-messages');
    var input = document.getElementById('cc-kmdb-input');
    var boton = document.getElementById('cc-kmdb-enviar');
    var chatUrl = form.dataset.chatUrl;
    var csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;
    var historial = [];

    function agregarMensaje(texto, tipo) {
        var burbuja = document.createElement('div');
        burbuja.className = 'cc-kmdb-msg cc-kmdb-msg-' + tipo;
        burbuja.textContent = texto;
        lista.appendChild(burbuja);
        lista.scrollTop = lista.scrollHeight;
        return burbuja;
    }

    function ajustarAltura() {
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 160) + 'px';
    }

    input.addEventListener('input', ajustarAltura);

    input.addEventListener('keydown', function (event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            form.requestSubmit();
        }
    });

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        var pregunta = input.value.trim();
        if (!pregunta) return;

        agregarMensaje(pregunta, 'user');
        input.value = '';
        ajustarAltura();
        input.disabled = true;
        boton.disabled = true;
        var espera = agregarMensaje('Pensando…', 'bot cc-kmdb-msg-espera');

        fetch(chatUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify({ mensaje: pregunta, historial: historial }),
        })
            .then(function (response) {
                return response.json().then(function (datos) {
                    return { ok: response.ok, datos: datos };
                });
            })
            .then(function (resultado) {
                espera.remove();
                if (!resultado.ok) {
                    agregarMensaje(resultado.datos.error || 'Ocurrió un error al consultar al asistente.', 'error');
                    return;
                }
                agregarMensaje(resultado.datos.respuesta, 'bot');
                historial.push({ role: 'user', content: pregunta });
                historial.push({ role: 'assistant', content: resultado.datos.respuesta });
            })
            .catch(function () {
                espera.remove();
                agregarMensaje('No se pudo conectar con el asistente. Revisa tu conexión e intenta de nuevo.', 'error');
            })
            .finally(function () {
                input.disabled = false;
                boton.disabled = false;
                input.focus();
            });
    });
});
