from django import forms
from django.contrib.auth.forms import PasswordChangeForm

from .models import Caso, Contacto, Correo, Documento, Sistema

_INPUT = 'cc-login-input'


class CambiarClaveForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = _INPUT


class SistemaForm(forms.ModelForm):
    class Meta:
        model = Sistema
        fields = ['nombre', 'descripcion', 'url', 'programa']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': _INPUT}),
            'descripcion': forms.TextInput(attrs={'class': _INPUT}),
            'url': forms.TextInput(attrs={'class': _INPUT}),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['nombre', 'descripcion', 'archivo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': _INPUT}),
            'descripcion': forms.TextInput(attrs={'class': _INPUT}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # En edición se conserva el archivo actual si no se sube uno nuevo.
        if self.instance.pk:
            self.fields['archivo'].required = False


class CorreoForm(forms.ModelForm):
    class Meta:
        model = Correo
        fields = ['titulo', 'asunto', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': _INPUT}),
            'asunto': forms.TextInput(attrs={'class': _INPUT}),
            'descripcion': forms.Textarea(attrs={'class': _INPUT, 'rows': 4}),
        }


class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ['titulo', 'descripcion']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': _INPUT}),
            'descripcion': forms.Textarea(attrs={'class': _INPUT, 'rows': 4}),
        }


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['titulo', 'descripcion', 'numero', 'extension']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': _INPUT}),
            'descripcion': forms.Textarea(attrs={'class': _INPUT, 'rows': 4}),
            'numero': forms.TextInput(attrs={'class': _INPUT}),
        }
