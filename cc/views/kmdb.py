from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def kmdb(request):
    if request.method == 'POST':
        # Procesar el formulario, guardar datos, etc.
        return redirect('kmdb')
    else:
        return render(request, 'cc/kmdb/kmdb.html', {'modulo_activo': 'kmdb'})
