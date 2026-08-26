from ..models import Contacto, ContextoIA, Servicio

_LARGO_MAX_DOCUMENTO = 6000  # caracteres por documento, para no disparar el tamaño del contexto


def _seccion(titulo, items, formato):
    if not items:
        return ''
    cuerpo = '\n'.join(formato(item) for item in items)
    return f'## {titulo}\n{cuerpo}\n'


def _sistema_a_texto(sistema):
    acceso = 'programa instalado' if sistema.programa else (sistema.url or 'sin URL registrada')
    return f'- {sistema.nombre}: {sistema.descripcion or "sin descripción"} ({acceso})'


def _correo_a_texto(correo):
    return f'- {correo.titulo} (Asunto: {correo.asunto}): {correo.descripcion or "sin descripción"}'


def _caso_a_texto(caso):
    return f'- {caso.titulo}: {caso.descripcion or "sin descripción"}'


def _contacto_a_texto(contacto):
    numero = contacto.numero or 'sin número'
    return f'- {contacto.titulo} ({numero}): {contacto.descripcion or "sin descripción"}'


def _documento_a_texto(documento):
    encabezado = f'### Documento: {documento.nombre}\n{documento.descripcion or "sin descripción"}'
    texto = (documento.contenido_texto or '')[:_LARGO_MAX_DOCUMENTO]
    if not texto:
        return encabezado
    return f'{encabezado}\n{texto}'


def _contexto_extra_a_texto(contexto):
    return f'### {contexto.titulo}\n{contexto.contenido}'


def construir_contexto():
    """Arma el texto con toda la información del sistema (servicios, sistemas,
    documentos, correos, casos, contactos y contexto adicional cargado a mano)
    que se pasa como contexto al chatbot de KMDB. Se reconstruye en cada
    consulta, así siempre refleja el estado actual de la base de datos.
    """
    partes = []

    for servicio in Servicio.objects.filter(activo=True).order_by('nombre'):
        partes.append(f'# Servicio: {servicio.nombre} ({servicio.codigo})\n{servicio.descripcion or ""}')
        partes.append(_seccion('Sistemas', list(servicio.sistemas.all()), _sistema_a_texto))
        for documento in servicio.documentos.all():
            partes.append(_documento_a_texto(documento))
        partes.append(_seccion('Correos', list(servicio.correos.all()), _correo_a_texto))
        partes.append(_seccion('Casos', list(servicio.casos.all()), _caso_a_texto))

    partes.append(_seccion('Contactos', list(Contacto.objects.all()), _contacto_a_texto))

    contextos_extra = list(ContextoIA.objects.filter(activo=True))
    if contextos_extra:
        partes.append('# Contexto adicional')
        for contexto in contextos_extra:
            partes.append(_contexto_extra_a_texto(contexto))

    return '\n\n'.join(parte for parte in partes if parte and parte.strip())
