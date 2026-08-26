from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from ..forms import CasoForm, CorreoForm, DocumentoForm, SistemaForm
from ..models import Caso, Correo, Documento, Servicio, Sistema

_CODIGO = 'EMPRESA'
_MODULO = 'empresa'
_TEMPLATE = 'cc/empresa/empresa.html'

_SECCION_POR_RECURSO = {'sistema': 'sistemas', 'documento': 'documentos', 'correo': 'correos', 'caso': 'casos'}
_SECCIONES_VALIDAS = set(_SECCION_POR_RECURSO.values())


def _contexto(servicio, **extra):
    context = {
        'modulo_activo': _MODULO,
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


def _redirect_seccion(recurso):
    return redirect(f'{reverse(_MODULO)}?seccion={_SECCION_POR_RECURSO[recurso]}')


@login_required
def empresa(request):
    servicio = get_object_or_404(Servicio, codigo=_CODIGO)

    if request.method == 'POST':
        accion = request.POST.get('accion', '')

        if accion == 'crear_sistema':
            form = SistemaForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.servicio = servicio
                obj.save()
                return _redirect_seccion('sistema')
            return render(request, _TEMPLATE, _contexto(
                servicio, sistema_form=form, open_modal='sistema', seccion_activa='sistemas'))

        elif accion == 'editar_sistema':
            instancia = get_object_or_404(Sistema, pk=request.POST.get('sistema_id'), servicio=servicio)
            form = SistemaForm(request.POST, request.FILES, instance=instancia)
            if form.is_valid():
                form.save()
                return _redirect_seccion('sistema')
            return render(request, _TEMPLATE, _contexto(
                servicio, sistema_form=form, sistema_id=instancia.pk, open_modal='sistema', seccion_activa='sistemas'))

        elif accion == 'eliminar_sistema':
            get_object_or_404(Sistema, pk=request.POST.get('sistema_id'), servicio=servicio).delete()
            return _redirect_seccion('sistema')

        elif accion == 'crear_documento':
            form = DocumentoForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.servicio = servicio
                obj.save()
                return _redirect_seccion('documento')
            return render(request, _TEMPLATE, _contexto(
                servicio, documento_form=form, open_modal='documento', seccion_activa='documentos'))

        elif accion == 'editar_documento':
            instancia = get_object_or_404(Documento, pk=request.POST.get('documento_id'), servicio=servicio)
            form = DocumentoForm(request.POST, request.FILES, instance=instancia)
            if form.is_valid():
                form.save()
                return _redirect_seccion('documento')
            return render(request, _TEMPLATE, _contexto(
                servicio, documento_form=form, documento_id=instancia.pk, open_modal='documento', seccion_activa='documentos'))

        elif accion == 'eliminar_documento':
            get_object_or_404(Documento, pk=request.POST.get('documento_id'), servicio=servicio).delete()
            return _redirect_seccion('documento')

        elif accion == 'crear_correo':
            form = CorreoForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.servicio = servicio
                obj.save()
                return _redirect_seccion('correo')
            return render(request, _TEMPLATE, _contexto(
                servicio, correo_form=form, open_modal='correo', seccion_activa='correos'))

        elif accion == 'editar_correo':
            instancia = get_object_or_404(Correo, pk=request.POST.get('correo_id'), servicio=servicio)
            form = CorreoForm(request.POST, instance=instancia)
            if form.is_valid():
                form.save()
                return _redirect_seccion('correo')
            return render(request, _TEMPLATE, _contexto(
                servicio, correo_form=form, correo_id=instancia.pk, open_modal='correo', seccion_activa='correos'))

        elif accion == 'eliminar_correo':
            get_object_or_404(Correo, pk=request.POST.get('correo_id'), servicio=servicio).delete()
            return _redirect_seccion('correo')

        elif accion == 'crear_caso':
            form = CasoForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.servicio = servicio
                obj.save()
                return _redirect_seccion('caso')
            return render(request, _TEMPLATE, _contexto(
                servicio, caso_form=form, open_modal='caso', seccion_activa='casos'))

        elif accion == 'editar_caso':
            instancia = get_object_or_404(Caso, pk=request.POST.get('caso_id'), servicio=servicio)
            form = CasoForm(request.POST, instance=instancia)
            if form.is_valid():
                form.save()
                return _redirect_seccion('caso')
            return render(request, _TEMPLATE, _contexto(
                servicio, caso_form=form, caso_id=instancia.pk, open_modal='caso', seccion_activa='casos'))

        elif accion == 'eliminar_caso':
            get_object_or_404(Caso, pk=request.POST.get('caso_id'), servicio=servicio).delete()
            return _redirect_seccion('caso')

        return redirect(_MODULO)

    contexto_extra = {}
    recurso = request.GET.get('abrir')
    pk = request.GET.get('id')

    if recurso == 'sistema' and pk:
        instancia = get_object_or_404(Sistema, pk=pk, servicio=servicio)
        contexto_extra['sistema_form'] = SistemaForm(instance=instancia)
        contexto_extra['sistema_id'] = pk
        contexto_extra['open_modal'] = 'sistema'
    elif recurso == 'documento' and pk:
        contexto_extra['abrir_documento'] = get_object_or_404(Documento, pk=pk, servicio=servicio)
    elif recurso == 'correo' and pk:
        contexto_extra['abrir_correo'] = get_object_or_404(Correo, pk=pk, servicio=servicio)
    elif recurso == 'caso' and pk:
        contexto_extra['abrir_caso'] = get_object_or_404(Caso, pk=pk, servicio=servicio)

    seccion = request.GET.get('seccion')
    if seccion not in _SECCIONES_VALIDAS:
        seccion = _SECCION_POR_RECURSO.get(recurso)
    contexto_extra['seccion_activa'] = seccion

    return render(request, _TEMPLATE, _contexto(servicio, **contexto_extra))
