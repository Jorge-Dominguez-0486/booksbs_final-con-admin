from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from tienda.models import Pedido, Libro, Genero, Autor
from .forms import LibroForm, UserForm, GeneroForm, AutorForm
from django.db.models import Q
from decimal import Decimal, InvalidOperation

def es_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(es_admin)
def vista_ver_pedidos(request):
    query = request.GET.get('q')
    pedidos = Pedido.objects.all()
    
    if query:
        search_filter = Q()
        is_numeric_search = False
        
        try:
            query_int = int(query)
            search_filter |= Q(id=query_int)
            is_numeric_search = True
        except ValueError:
            pass
            
        try:
            query_dec = Decimal(query)
            search_filter |= Q(total_pagado=query_dec)
            is_numeric_search = True
        except InvalidOperation:
            pass
        
        # Si la consulta NO FUE numérica, busca en campos de texto/fecha
        if not is_numeric_search:
            search_filter = (
                Q(usuario__email__icontains=query) |
                Q(usuario__first_name__icontains=query) |
                Q(estado_pago__icontains=query) |
                Q(fecha_pedido__icontains=query) # Búsqueda de fecha como texto
            )
            
        pedidos = pedidos.filter(search_filter).order_by('-fecha_pedido').distinct()
    else:
        pedidos = pedidos.order_by('-fecha_pedido')
        
    contexto = {
        'pedidos': pedidos,
        'search_query': query
    }
    return render(request, 'dashboard/ver_pedidos.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_ver_libros(request):
    query = request.GET.get('q')
    libros = Libro.objects.all()
    
    if query:
        search_filter = Q()
        is_numeric_search = False

        try:
            # Intenta buscar por ID
            query_int = int(query)
            search_filter |= Q(id=query_int)
            is_numeric_search = True
        except ValueError:
            pass # No es un entero

        try:
            # Intenta buscar por Precio
            query_dec = Decimal(query)
            search_filter |= Q(precio=query_dec)
            is_numeric_search = True
        except InvalidOperation:
            pass # No es un decimal
        
        # Si NO fue una búsqueda numérica, entonces busca en el texto
        if not is_numeric_search:
            search_filter = (
                Q(titulo__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(estado_publicacion__icontains=query) |
                Q(formato__icontains=query) |
                Q(autores__nombre_autor__icontains=query) |
                Q(generos__nombre_genero__icontains=query)
            )
            
        libros = libros.filter(search_filter).order_by('id').distinct()
    else:
        libros = libros.order_by('id')
        
    contexto = {
        'libros': libros,
        'search_query': query
    }
    return render(request, 'dashboard/ver_libros.html', contexto)

# --- Vistas de Libros (Agregar, Editar, Borrar) - Sin cambios ---

@login_required
@user_passes_test(es_admin)
def vista_agregar_libro(request):
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Libro agregado exitosamente!')
            return redirect('dash_ver_libros')
        else:
            messages.error(request, 'Hubo un error. Revisa el formulario.')
    else:
        form = LibroForm()
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Agregar Nuevo Libro'
    }
    return render(request, 'dashboard/form_generico.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_editar_libro(request, id_libro):
    libro = get_object_or_404(Libro, id=id_libro)
    if request.method == 'POST':
        form = LibroForm(request.POST, request.FILES, instance=libro)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Libro actualizado exitosamente!')
            return redirect('dash_ver_libros')
        else:
            messages.error(request, 'Hubo un error. Revisa el formulario.')
    else:
        form = LibroForm(instance=libro)
    
    contexto = {
        'form': form,
        'titulo_pagina': f'Editar Libro: {libro.titulo}'
    }
    return render(request, 'dashboard/form_generico.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_borrar_libro(request, id_libro):
    libro = get_object_or_404(Libro, id=id_libro)
    if request.method == 'POST':
        libro.delete()
        messages.success(request, f"El libro '{libro.titulo}' ha sido eliminado.")
        return redirect('dash_ver_libros')
    
    contexto = {
        'objeto': libro,
        'titulo_pagina': 'Borrar Libro',
        'url_cancelar': 'dash_ver_libros'
    }
    return render(request, 'dashboard/borrar_generico.html', contexto)

# --- Vistas de Usuarios ---

@login_required
@user_passes_test(es_admin)
def vista_ver_usuarios(request):
    query = request.GET.get('q')
    usuarios = User.objects.all()
    
    if query:
        search_filter = Q()
        is_numeric_search = False

        try:
            query_int = int(query)
            search_filter |= Q(id=query_int)
            is_numeric_search = True
        except ValueError:
            pass
        
        # Si no es numérico, busca en campos de texto
        if not is_numeric_search:
            search_filter = (
                Q(email__icontains=query) | 
                Q(first_name__icontains=query) | 
                Q(username__icontains=query)
            )
            
        usuarios = usuarios.filter(search_filter).order_by('id').distinct()
    else:
        usuarios = usuarios.order_by('id')
        
    contexto = {
        'usuarios': usuarios,
        'search_query': query
    }
    return render(request, 'dashboard/ver_usuarios.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_editar_usuario(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Usuario actualizado exitosamente!')
            return redirect('dash_ver_usuarios')
        else:
            messages.error(request, 'Hubo un error. Revisa el formulario.')
    else:
        form = UserForm(instance=usuario)
    
    contexto = {
        'form': form,
        'titulo_pagina': f'Editar Usuario: {usuario.username}'
    }
    return render(request, 'dashboard/form_generico.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_borrar_usuario(request, id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
    if usuario.is_superuser:
        messages.error(request, 'No puedes eliminar a un Superusuario.')
        return redirect('dash_ver_usuarios')
        
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, f"El usuario '{usuario.username}' ha sido eliminado.")
        return redirect('dash_ver_usuarios')
    
    contexto = {
        'objeto': usuario,
        'titulo_pagina': 'Borrar Usuario',
        'url_cancelar': 'dash_ver_usuarios'
    }
    return render(request, 'dashboard/borrar_generico.html', contexto)

# --- Vistas de Géneros ---

@login_required
@user_passes_test(es_admin)
def vista_ver_generos(request):
    query = request.GET.get('q')
    generos = Genero.objects.all()
    
    if query:
        search_filter = Q()
        is_numeric_search = False

        try:
            query_int = int(query)
            search_filter |= Q(id=query_int)
            is_numeric_search = True
        except ValueError:
            pass
            
        # Si no es numérico, busca en campos de texto
        if not is_numeric_search:
            search_filter = (
                Q(nombre_genero__icontains=query) |
                Q(descripcion_genero__icontains=query)
            )
        
        generos = generos.filter(search_filter).order_by('nombre_genero').distinct()
    else:
        generos = generos.order_by('nombre_genero')
        
    contexto = {
        'generos': generos,
        'search_query': query
    }
    return render(request, 'dashboard/ver_generos.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_agregar_genero(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Género agregado exitosamente!')
            return redirect('dash_ver_generos')
    else:
        form = GeneroForm()
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Agregar Nuevo Género'
    }
    return render(request, 'dashboard/form_generico.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_editar_genero(request, id_genero):
    genero = get_object_or_404(Genero, id=id_genero)
    if request.method == 'POST':
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Género actualizado exitosamente!')
            return redirect('dash_ver_generos')
    else:
        form = GeneroForm(instance=genero)
    
    contexto = {
        'form': form,
        'titulo_pagina': f'Editar Género: {genero.nombre_genero}'
    }
    return render(request, 'dashboard/form_generico.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_borrar_genero(request, id_genero):
    genero = get_object_or_404(Genero, id=id_genero)
    if request.method == 'POST':
        genero.delete()
        messages.success(request, f"El género '{genero.nombre_genero}' ha sido eliminado.")
        return redirect('dash_ver_generos')
    
    contexto = {
        'objeto': genero,
        'titulo_pagina': 'Borrar Género',
        'url_cancelar': 'dash_ver_generos'
    }
    return render(request, 'dashboard/borrar_generico.html', contexto)

# --- Vistas de Autores ---

@login_required
@user_passes_test(es_admin)
def vista_ver_autores(request):
    query = request.GET.get('q')
    autores = Autor.objects.all()
    
    if query:
        search_filter = Q()
        is_numeric_search = False

        try:
            query_int = int(query)
            search_filter |= Q(id=query_int)
            is_numeric_search = True
        except ValueError:
            pass
        
        # Si no es numérico, busca en campos de texto
        if not is_numeric_search:
            search_filter = (
                Q(nombre_autor__icontains=query) |
                Q(biografia__icontains=query)
            )
        
        autores = autores.filter(search_filter).order_by('nombre_autor').distinct()
    else:
        autores = autores.order_by('nombre_autor')

    contexto = {
        'autores': autores,
        'search_query': query
    }
    return render(request, 'dashboard/ver_autores.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_agregar_autor(request):
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Autor agregado exitosamente!')
            return redirect('dash_ver_autores')
    else:
        form = AutorForm()
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Agregar Nuevo Autor'
    }
    return render(request, 'dashboard/form_generico.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_editar_autor(request, id_autor):
    autor = get_object_or_404(Autor, id=id_autor)
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES, instance=autor)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Autor actualizado exitosamente!')
            return redirect('dash_ver_autores')
    else:
        form = AutorForm(instance=autor)
    
    contexto = {
        'form': form,
        'titulo_pagina': f'Editar Autor: {autor.nombre_autor}'
    }
    return render(request, 'dashboard/form_generico.html', contexto)

@login_required
@user_passes_test(es_admin)
def vista_borrar_autor(request, id_autor):
    autor = get_object_or_404(Autor, id=id_autor)
    if request.method == 'POST':
        autor.delete()
        messages.success(request, f"El autor '{autor.nombre_autor}' ha sido eliminado.")
        return redirect('dash_ver_autores')
    
    contexto = {
        'objeto': autor,
        'titulo_pagina': 'Borrar Autor',
        'url_cancelar': 'dash_ver_autores'
    }
    return render(request, 'dashboard/borrar_generico.html', contexto)