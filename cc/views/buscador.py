from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse

from ..models import Caso, Contacto, Correo, Documento, Sistema

_MODULO_URL = {
    'EMPRESA': 'empresa',
    'BARRIO': 'barrio',
    'CLARO': 'claro',
}

_LIMITE_POR_TIPO = 8
_LIMITE_TOTAL = 20


def _buscar_en(model, termino, *campos):
    query = Q()
    for campo in campos:
        query |= Q(**{f'{campo}__icontains': termino})
    queryset = model.objects.filter(query)
    if hasattr(model, 'servicio'):
        queryset = queryset.select_related('servicio')
    return queryset[:_LIMITE_POR_TIPO]


def _url_registro(url_name, recurso, pk):
    return f"{reverse(url_name)}?{urlencode({'abrir': recurso, 'id': pk})}"


@login_required
def buscar(request):
    termino = request.GET.get('q', '').strip()
    resultados = []

    if len(termino) >= 2:
        for sistema in _buscar_en(Sistema, termino, 'nombre', 'descripcion', 'url'):
            url_name = _MODULO_URL[sistema.servicio.codigo]
            resultados.append({
                'tipo': 'Sistema',
                'titulo': sistema.nombre,
                'subtitulo': sistema.servicio.nombre,
                'url': _url_registro(url_name, 'sistema', sistema.pk),
            })
        for documento in _buscar_en(Documento, termino, 'nombre', 'descripcion'):
            url_name = _MODULO_URL[documento.servicio.codigo]
            resultados.append({
                'tipo': 'Documento',
                'titulo': documento.nombre,
                'subtitulo': documento.servicio.nombre,
                'url': _url_registro(url_name, 'documento', documento.pk),
            })
        for correo in _buscar_en(Correo, termino, 'titulo', 'asunto', 'descripcion'):
            url_name = _MODULO_URL[correo.servicio.codigo]
            resultados.append({
                'tipo': 'Correo',
                'titulo': correo.titulo,
                'subtitulo': correo.servicio.nombre,
                'url': _url_registro(url_name, 'correo', correo.pk),
            })
        for caso in _buscar_en(Caso, termino, 'titulo', 'descripcion'):
            url_name = _MODULO_URL[caso.servicio.codigo]
            resultados.append({
                'tipo': 'Caso',
                'titulo': caso.titulo,
                'subtitulo': caso.servicio.nombre,
                'url': _url_registro(url_name, 'caso', caso.pk),
            })
        for contacto in _buscar_en(Contacto, termino, 'titulo', 'descripcion', 'numero'):
            resultados.append({
                'tipo': 'Contacto',
                'titulo': contacto.titulo,
                'subtitulo': contacto.numero or contacto.descripcion or '—',
                'url': _url_registro('contactos', 'contacto', contacto.pk),
            })

    return JsonResponse({'resultados': resultados[:_LIMITE_TOTAL]})
