from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..forms import CasoForm, CorreoForm, DocumentoForm, SistemaForm
from ..models import Caso, Correo, Documento, Servicio, Sistema

_RECURSOS = {
    'sistema': (Sistema, SistemaForm),
    'documento': (Documento, DocumentoForm),
    'correo': (Correo, CorreoForm),
    'caso': (Caso, CasoForm),
}

# Recursos cuyo enlace de búsqueda abre el formulario de edición. Documento y
# correo/caso tienen una acción más útil desde el buscador (vista previa y
# "usar plantilla" respectivamente), ver `vista_modulo`.
_RECURSOS_EDITABLES = {'sistema'}

# Sección (parámetro ?seccion=) a la que pertenece cada recurso, usada por las
# plantillas que muestran las 4 secciones detrás de cards en vez de todas
# apiladas (ver empresa.html). Los módulos que no distinguen secciones
# simplemente ignoran `seccion_activa` en el contexto.
_SECCION_POR_RECURSO = {clave: f'{clave}s' for clave in _RECURSOS}
_SECCIONES_VALIDAS = set(_SECCION_POR_RECURSO.values())


def contexto_modulo(servicio, modulo_activo, **extra):
    context = {
        'modulo_activo': modulo_activo,
        'servicio': servicio,
        'sistemas': servicio.sistemas.all(),
        'documentos': servicio.documentos.all(),
        'correos': servicio.correos.all(),
        'casos': servicio.casos.all(),
        'sistema_form': SistemaForm(),
        'documento_form': DocumentoForm(),
        'correo_form': CorreoForm(),
        'caso_form': CasoForm(),
        'open_modal': None,
    }
    context.update(extra)
    return context


def vista_modulo(request, codigo, modulo_activo, template):
    servicio = get_object_or_404(Servicio, codigo=codigo)
    if request.method == 'POST':
        return redirect(modulo_activo)

    contexto_extra = {}
    recurso = request.GET.get('abrir')
    pk = request.GET.get('id')
    datos = _RECURSOS.get(recurso)

    if datos and pk:
        model, form_class = datos
        instancia = get_object_or_404(model, pk=pk, servicio=servicio)
        if recurso in _RECURSOS_EDITABLES:
            contexto_extra[f'{recurso}_form'] = form_class(instance=instancia)
            contexto_extra[f'{recurso}_id'] = pk
            contexto_extra['open_modal'] = recurso
        else:
            # documento -> vista previa, correo/caso -> usar plantilla.
            contexto_extra[f'abrir_{recurso}'] = instancia

    seccion = request.GET.get('seccion')
    if seccion not in _SECCIONES_VALIDAS:
        seccion = _SECCION_POR_RECURSO.get(recurso)
    contexto_extra['seccion_activa'] = seccion

    return render(request, template, contexto_modulo(servicio, modulo_activo, **contexto_extra))


def procesar_recurso(request, codigo, modulo_activo, template, model, form_class, key):
    """Crea, edita o elimina un sub-recurso (Sistema/Documento/Correo/Caso) de un módulo.

    El modal siempre envía al mismo endpoint: `action` = 'guardar' o
    'eliminar', e `id` = vacío (crear) o el pk del registro (editar/eliminar).
    """
    servicio = get_object_or_404(Servicio, codigo=codigo)
    action = request.POST.get('action', 'guardar')
    pk = request.POST.get('id') or None
    seccion = _SECCION_POR_RECURSO.get(key, key)

    if action == 'eliminar':
        get_object_or_404(model, pk=pk, servicio=servicio).delete()
        return redirect(f'{reverse(modulo_activo)}?seccion={seccion}')

    instance = get_object_or_404(model, pk=pk, servicio=servicio) if pk else None
    form = form_class(request.POST, request.FILES, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.servicio = servicio
        obj.save()
        return redirect(f'{reverse(modulo_activo)}?seccion={seccion}')

    context = contexto_modulo(servicio, modulo_activo, seccion_activa=seccion)
    context[f'{key}_form'] = form
    context[f'{key}_id'] = pk
    context['open_modal'] = key
    return render(request, template, context)
