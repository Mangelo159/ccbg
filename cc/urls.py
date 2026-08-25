from django.urls import path

from .views.barrio import barrio
from .views.buscador import buscar
from .views.claro import claro
from .views.contactos import contactos
from .views.empresa import empresa
from .views.kmdb import kmdb
from .views.view import cambiar_clave, home, login_view, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('cambiar-clave', cambiar_clave, name='cambiar_clave'),
    path('buscar', buscar, name='buscar'),

    path('empresa', empresa, name='empresa'),

    path('barrio', barrio, name='barrio'),

    path('claro', claro, name='claro'),

    path('contactos', contactos, name='contactos'),
    path('kmdb', kmdb, name='kmdb'),
]
