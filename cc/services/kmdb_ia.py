import anthropic
from django.conf import settings

from .kmdb_contexto import construir_contexto

_MODELO = 'claude-sonnet-5'
_MAX_TOKENS = 1024

_INSTRUCCIONES = (
    'Eres el asistente interno de KMDB en Custome Care. Respondes preguntas del equipo de soporte '
    'usando ÚNICAMENTE la información del sistema que se te entrega a continuación (servicios, sistemas, '
    'documentos, correos, casos y contactos). Si la respuesta no está en esa información, dilo con claridad '
    'en vez de inventar. Sé conciso y, cuando ayude, indica de qué servicio o documento sale cada dato.'
)

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _client


def preguntar(pregunta, historial=None):
    """Envía una pregunta a Claude junto con el contexto del KMDB.

    `historial` es una lista de mensajes previos ({'role': ..., 'content': ...})
    tal como los devuelve/consume la API de Anthropic; el llamador es responsable
    de mantenerla entre turnos (no se persiste en el servidor).
    """
    system = [
        {'type': 'text', 'text': _INSTRUCCIONES},
        {'type': 'text', 'text': construir_contexto(), 'cache_control': {'type': 'ephemeral'}},
    ]

    mensajes = list(historial or []) + [{'role': 'user', 'content': pregunta}]

    respuesta = _get_client().messages.create(
        model=_MODELO,
        max_tokens=_MAX_TOKENS,
        system=system,
        messages=mensajes,
    )

    return next((bloque.text for bloque in respuesta.content if bloque.type == 'text'), '')
