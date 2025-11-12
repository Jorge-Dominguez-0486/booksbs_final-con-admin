from django.urls import path
from . import views

urlpatterns = [
    path('pedidos/', views.vista_ver_pedidos, name='dash_ver_pedidos'),
    
    path('libros/', views.vista_ver_libros, name='dash_ver_libros'),
    path('libros/agregar/', views.vista_agregar_libro, name='dash_agregar_libro'),
    path('libros/editar/<int:id_libro>/', views.vista_editar_libro, name='dash_editar_libro'),
    path('libros/borrar/<int:id_libro>/', views.vista_borrar_libro, name='dash_borrar_libro'),
    
    path('usuarios/', views.vista_ver_usuarios, name='dash_ver_usuarios'),
    path('usuarios/editar/<int:id_usuario>/', views.vista_editar_usuario, name='dash_editar_usuario'),
    path('usuarios/borrar/<int:id_usuario>/', views.vista_borrar_usuario, name='dash_borrar_usuario'),

    path('generos/', views.vista_ver_generos, name='dash_ver_generos'),
    path('generos/agregar/', views.vista_agregar_genero, name='dash_agregar_genero'),
    path('generos/editar/<int:id_genero>/', views.vista_editar_genero, name='dash_editar_genero'),
    path('generos/borrar/<int:id_genero>/', views.vista_borrar_genero, name='dash_borrar_genero'),

    path('autores/', views.vista_ver_autores, name='dash_ver_autores'),
    path('autores/agregar/', views.vista_agregar_autor, name='dash_agregar_autor'),
    path('autores/editar/<int:id_autor>/', views.vista_editar_autor, name='dash_editar_autor'),
    path('autores/borrar/<int:id_autor>/', views.vista_borrar_autor, name='dash_borrar_autor'),
]