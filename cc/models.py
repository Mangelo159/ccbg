from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.db import models


class Servicio(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    icono = models.CharField(max_length=50, blank=True, help_text='Nombre del ícono SVG')
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.nombre


class Sistema(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='sistemas')
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True)
    url = models.CharField(max_length=200, blank=True)
    programa = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Sistema'
        verbose_name_plural = 'Sistemas'

    def __str__(self):
        return self.nombre


class Documento(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='documentos')
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True)
    archivo = models.FileField(upload_to='documentos/', storage=RawMediaCloudinaryStorage())

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

    def __str__(self):
        return self.nombre


class Correo(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='correos')
    titulo = models.CharField(max_length=100)
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Correo'
        verbose_name_plural = 'Correos'

    def __str__(self):
        return self.titulo


class Caso(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='casos')
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Caso'
        verbose_name_plural = 'Casos'

    def __str__(self):
        return self.titulo


class Contacto(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    numero = models.CharField(max_length=20, blank=True)
    extension = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

    def __str__(self):
        return self.titulo