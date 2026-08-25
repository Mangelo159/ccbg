from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from ..forms import CasoForm, CorreoForm, DocumentoForm, SistemaForm
from ..models import Caso, Correo, Documento, Sistema
from ._servicio_crud import procesar_recurso, vista_modulo

_CODIGO = 'CLARO'
_MODULO = 'claro'
_TEMPLATE = 'cc/claro/claro.html'

_RECURSOS = {
    'sistema': (Sistema, SistemaForm),
    'documento': (Documento, DocumentoForm),
    'correo': (Correo, CorreoForm),
    'caso': (Caso, CasoForm),
}


@login_required
def claro(request):
    if request.method != 'POST':
        return vista_modulo(request, _CODIGO, _MODULO, _TEMPLATE)

    nombre_recurso = request.POST.get('recurso')
    datos = _RECURSOS.get(nombre_recurso)
    if datos is None:
        return redirect(_MODULO)

    model, form_class = datos
    return procesar_recurso(request, _CODIGO, _MODULO, _TEMPLATE, model, form_class, nombre_recurso)
