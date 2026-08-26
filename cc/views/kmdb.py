import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from ..forms import ContextoIAForm
from ..models import ContextoIA
from ..services.kmdb_ia import preguntar

_TEMPLATE = 'cc/kmdb/kmdb.html'
_ACCIONES_CONTEXTO = {'crear_contexto', 'editar_contexto', 'eliminar_contexto'}


def _contexto(request, **extra):
    context = {
        'modulo_activo': 'kmdb',
        'open_modal': None,
    }
    if request.user.is_superuser:
        context['contextos'] = ContextoIA.objects.all()
        context['contexto_form'] = ContextoIAForm()
    context.update(extra)
    return context


@login_required
def kmdb(request):
    if request.method == 'POST':
        accion = request.POST.get('accion', '')

        if accion in _ACCIONES_CONTEXTO and not request.user.is_superuser:
            return HttpResponseForbidden('No tienes permiso para modificar el contexto del chatbot.')

        if accion == 'crear_contexto':
            form = ContextoIAForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('kmdb')
            return render(request, _TEMPLATE, _contexto(request, contexto_form=form, open_modal='contexto'))

        elif accion == 'editar_contexto':
            instancia = get_object_or_404(ContextoIA, pk=request.POST.get('contexto_id'))
            form = ContextoIAForm(request.POST, instance=instancia)
            if form.is_valid():
                form.save()
                return redirect('kmdb')
            return render(request, _TEMPLATE, _contexto(
                request, contexto_form=form, contexto_id=instancia.pk, open_modal='contexto'))

        elif accion == 'eliminar_contexto':
            get_object_or_404(ContextoIA, pk=request.POST.get('contexto_id')).delete()
            return redirect('kmdb')

        return redirect('kmdb')

    return render(request, _TEMPLATE, _contexto(request))


@login_required
@require_POST
def kmdb_chat(request):
    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({'error': 'Solicitud inválida.'}, status=400)

    pregunta = (datos.get('mensaje') or '').strip()
    historial = datos.get('historial') or []
    if not pregunta:
        return JsonResponse({'error': 'Escribe una pregunta.'}, status=400)

    try:
        respuesta = preguntar(pregunta, historial)
    except Exception:
        return JsonResponse({'error': 'No se pudo obtener respuesta del asistente. Intenta de nuevo en un momento.'}, status=502)

    return JsonResponse({'respuesta': respuesta})
