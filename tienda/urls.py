from django.urls import path
from . import views  

urlpatterns = [
    # Principales y Catálogo
    path('', views.pagina_index, name='index'),
    path('proximos/', views.pagina_proximos, name='proximos'),
    path('bookstore/', views.pagina_bookstore, name='bookstore'),
    
    # URLs Detalle SEPARADAS
    path('proximo/<int:id_libro>/', views.pagina_proximo_detalle, name='proximo_detalle'),
    path('libro/<int:id_libro>/', views.pagina_libro_detalle, name='libro_detalle'),

    # Autenticación
    path('login/', views.pagina_login, name='login'),
    path('registro/', views.pagina_registro, name='registro'),
    path('logout/', views.pagina_logout, name='logout'),

    # Vistas usuario
    path('cuenta/', views.pagina_cuenta, name='cuenta'),
    path('mis-libros/', views.pagina_mis_libros, name='mis_libros'),
    
   
    path('leer/<int:id_libro>/<int:pagina>/', views.pagina_leer_libro, name='leer_libro'),

    # Compra
    path('comprar/<int:id_libro>/', views.pagina_compra, name='compra'),
    path('procesar_compra/<int:id_libro>/', views.procesar_compra, name='procesar_compra'),
]