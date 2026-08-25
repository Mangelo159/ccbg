# Notas importantes del proyecto

## Stack
- Python 3.11.9
- Django 4.2 LTS
- Proyecto: `customecare`
- App: `cc`

## Requerimientos

### 1. Vista FBV con GET y POST en la misma función
> Quiero una vista basada en funciones (FBV) en Django que maneje GET y POST en la misma función, usando `if request.method == 'POST'` y `else` para GET.

Prueba de concepto inicial implementada en `cc/views/item.py` (`item_view`, ruta `/cc/item`) — **eliminada** tras crear los módulos reales (era solo demo, no un módulo del negocio).

**Patrón vigente** (aplicado a las 6 vistas reales — `home`, `empresa`, `barrio`, `claro`, `contactos`, `kmdb`): en vez de renderizar en el propio POST, cada vista redirige tras procesar (patrón Post/Redirect/Get):

```python
from django.shortcuts import redirect, render


def empresa(request):
    if request.method == 'POST':
        # Procesar el formulario, guardar datos, etc.
        return redirect('empresa')
    else:
        return render(request, 'cc/empresa/empresa.html', {'modulo_activo': 'empresa'})
```

Ruteo:
- `customecare/urls.py` incluye `cc/urls.py` en la **raíz** (`path('', include('cc.urls'))`, sin prefijo `cc/`)
- `cc/urls.py` mapea cada ruta sin slash final (`path('contactos', contactos, name='contactos')`, etc.), importando cada función directo desde su archivo (`cc/views/<modulo>.py`)
- URLs finales: `/` (home), `/login`, `/logout`, `/empresa`, `/barrio`, `/claro`, `/contactos`, `/kmdb`

### 2. Conexión a PostgreSQL
`DATABASES` en `customecare/settings.py` usa `django.db.backends.postgresql` con credenciales leídas vía `python-decouple` desde `.env` (no versionado, ver `.gitignore`). Plantilla de variables en `.env.example`.

Dependencias añadidas: `psycopg2-binary`, `python-decouple` (ver `requirements.txt`).

**Nota de troubleshooting (Windows + PostgreSQL con locale en español):** si `manage.py migrate` lanza `UnicodeDecodeError: 'utf-8' codec can't decode byte ... invalid continuation byte`, no es un problema de configuración de Django sino que psycopg2 en Windows no puede decodificar mensajes de error de PostgreSQL que vienen en español (colación `Spanish_*.1252` del servidor) cuando hay password incorrecto o la base no existe. Solución: verificar credenciales/nombre de base con `psql` directamente (bypassa el bug de decodificación) y corregir `.env`.

### 3. Modelos (`cc/models.py`)
6 modelos: `Servicio`, `Sistema`, `Documento`, `Correo`, `Caso`, `Contacto`. Todos los FK a `Servicio` se llaman `servicio` (antes tenían prefijos inconsistentes: `sservicio`, `dservicio`, `coservicio`, `caervicio`); cada modelo usa `related_name` distinto (`sistemas`, `documentos`, `correos`, `casos`) para no chocar en las relaciones inversas. `Servicio.codigo` es `unique=True`. `Contacto.extension` es intencionalmente `BooleanField`: indica si `numero` es una extensión interna o un número normal (no guarda el valor de la extensión).

Migración inicial: `cc/migrations/0001_initial.py`, aplicada.

### 4. Almacenamiento de archivos: Cloudinary
`Documento.archivo` (y cualquier otro `FileField`/`ImageField`) sube a Cloudinary en vez de al disco local, vía `django-cloudinary-storage`.

- `settings.py`: apps `cloudinary_storage` (antes de `staticfiles`) y `cloudinary`; `STORAGES['default']` → `cloudinary_storage.storage.MediaCloudinaryStorage`; credenciales en `CLOUDINARY_STORAGE` leídas de `.env` (`CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`).
- **Pendiente:** completar esas 3 variables en `.env` con las credenciales reales de https://cloudinary.com/console (Dashboard → Product Environment Credentials). Sin ellas, cualquier subida de archivo fallará en tiempo de ejecución (el proyecto arranca igual, `check`/`migrate` no lo requieren).

### 5. Deploy a Railway
- `Procfile`: fase `release` corre `migrate` automáticamente en cada deploy; `web` levanta `gunicorn customecare.wsgi`.
- `DATABASES` en `settings.py` usa `DATABASE_URL` (vía `dj-database-url`) si está presente — Railway la inyecta solo al agregar un servicio de Postgres; si no existe, cae a las variables `DB_*` individuales (para desarrollo local).
- Estáticos servidos con `whitenoise` (`STORAGES['staticfiles']` = `CompressedManifestStaticFilesStorage`, `STATIC_ROOT = staticfiles/`) — Railway no sirve estáticos por sí solo.
- `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` agregan automáticamente el dominio si Railway define `RAILWAY_PUBLIC_DOMAIN`.
- **Variables de entorno a configurar en el proyecto de Railway** (Settings → Variables): `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`. `DATABASE_URL` y `RAILWAY_PUBLIC_DOMAIN` los pone Railway solo.
- **Pendiente:** confirmar si se usa el Postgres que provisiona Railway (recomendado) o uno externo distinto al local ya configurado.

### 6. Templates: proyecto vs. app
`templates/` vive a nivel de proyecto (no dentro de `cc/`), tal como especifica `DESING-SISTEM.md` sección 8. Configurado en `settings.py` vía `TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']`. Estructura: `templates/base.html` (layout maestro) + `templates/cc/<modulo>/<modulo>.html` (una carpeta por módulo/página, arquitectura limpia). `static/` (con `static/css/cc.css`) también vive a nivel de proyecto, vía `STATICFILES_DIRS`.

### 7. Vistas: un archivo por vista (y `view.py` para home/login/logout)
`cc/views/` es un paquete, no un `views.py` único. Los 5 módulos de negocio tienen cada uno su propio archivo: `empresa.py`, `barrio.py`, `claro.py`, `contactos.py`, `kmdb.py`. `home`, `login_view` y `logout_view` están agrupados juntos en `cc/views/view.py` (a pedido explícito, van los tres en un solo archivo porque están relacionados con el flujo de entrada al portal). Todas se importan explícitamente en `cc/urls.py`. Rutas sin slash final: `path('contactos', contactos, name='contactos')`.

### 8. Login propio del portal
No estaba en `DESING-SISTEM.md`; se construyó siguiendo su misma paleta/tipografía porque el portal es de uso interno. Usa el sistema de auth de Django (`django.contrib.auth`, tabla `auth_user`) — sin modelo de usuario custom.

- `cc/views/login.py` (`login_view`) y `cc/views/logout.py` (`logout_view`), patrón POST→redirect / GET→render.
- Template independiente `templates/cc/login/login.html` (no extiende `base.html`: no lleva sidebar/header, es la pantalla previa a entrar).
- `home`, `empresa`, `barrio`, `claro`, `contactos`, `kmdb` protegidas con `@login_required` → sin sesión redirigen a `/cc/login?next=...`.
- `settings.py`: `LOGIN_URL='login'`, `LOGIN_REDIRECT_URL='home'`, `LOGOUT_REDIRECT_URL='login'`.
- El avatar del header/sidebar muestra la inicial del usuario autenticado (`request.user.username`); logout es un botón (ícono junto al avatar) que hace POST a `/logout`. `logout_view` cierra sesión con cualquier método (GET incluido) — entrar directo a `/logout` también cierra sesión.
- **Usuario de prueba creado en local:** `admin` / `CustomeCare2026!` (superusuario, vía `manage.py shell`). Cámbialo o crea el tuyo con `manage.py createsuperuser` antes de producción.
