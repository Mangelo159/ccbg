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
    if request.method == 'POST':
        accion = request.POST.get('accion', '')

        if accion == 'crear_contacto':
            form = ContactoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(_MODULO)
            return render(request, _TEMPLATE, _contexto(contacto_form=form, open_modal='contacto'))

        elif accion == 'editar_contacto':
            instancia = get_object_or_404(Contacto, pk=request.POST.get('contacto_id'))
            form = ContactoForm(request.POST, instance=instancia)
            if form.is_valid():
                form.save()
                return redirect(_MODULO)
            return render(request, _TEMPLATE, _contexto(
                contacto_form=form, contacto_id=instancia.pk, open_modal='contacto'))

        elif accion == 'eliminar_contacto':
            get_object_or_404(Contacto, pk=request.POST.get('contacto_id')).delete()
            return redirect(_MODULO)

        return redirect(_MODULO)

    contexto_extra = {}
    pk = request.GET.get('id')
    if request.GET.get('abrir') == 'contacto' and pk:
        instancia = get_object_or_404(Contacto, pk=pk)
        contexto_extra['contacto_form'] = ContactoForm(instance=instancia)
        contexto_extra['contacto_id'] = pk
        contexto_extra['open_modal'] = 'contacto'
    return render(request, _TEMPLATE, _contexto(**contexto_extra))
