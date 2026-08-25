from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from ..forms import ContactoForm
from ..models import Contacto

_MODULO = 'contactos'
_TEMPLATE = 'cc/contactos/contactos.html'


def _contexto(**extra):
    context = {
        'modulo_activo': _MODULO,
        'contactos': Contacto.objects.all(),
        'contacto_form': ContactoForm(),
        'open_modal': None,
    }
    context.update(extra)
    return context


@login_required
def contactos(request):
    if request.method != 'POST':
        contexto_extra = {}
        pk = request.GET.get('id')
        if request.GET.get('abrir') == 'contacto' and pk:
            instancia = get_object_or_404(Contacto, pk=pk)
            contexto_extra['contacto_form'] = ContactoForm(instance=instancia)
            contexto_extra['contacto_id'] = pk
            contexto_extra['open_modal'] = 'contacto'
        return render(request, _TEMPLATE, _contexto(**contexto_extra))

    action = request.POST.get('action', 'guardar')
    pk = request.POST.get('id') or None

    if action == 'eliminar':
        get_object_or_404(Contacto, pk=pk).delete()
        return redirect(_MODULO)

    instance = get_object_or_404(Contacto, pk=pk) if pk else None
    form = ContactoForm(request.POST, instance=instance)
    if form.is_valid():
        form.save()
        return redirect(_MODULO)

    context = _contexto(contacto_form=form, contacto_id=pk, open_modal='contacto')
    return render(request, _TEMPLATE, context)
