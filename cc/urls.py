from django.urls import re_path as url

from .views.barrio import barrio
from .views.buscador import buscar
from .views.claro import claro
from .views.contactos import contactos
from .views.empresa import empresa
from .views.kmdb import kmdb, kmdb_chat
from .views.view import cambiar_clave, home, login_view, logout_view

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login$', login_view, name='login'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^cambiar-clave$', cambiar_clave, name='cambiar_clave'),
    url(r'^buscar$', buscar, name='buscar'),

    url(r'^empresa$', empresa, name='empresa'),

    url(r'^barrio$', barrio, name='barrio'),

    url(r'^claro$', claro, name='claro'),

    url(r'^contactos$', contactos, name='contactos'),
    url(r'^kmdb$', kmdb, name='kmdb'),
    url(r'^kmdb/chat$', kmdb_chat, name='kmdb_chat'),
]
