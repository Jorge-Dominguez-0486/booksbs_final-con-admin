from django.shortcuts import render, get_object_or_404, redirect
from .models import Libro, Genero, Autor, BibliotecaUsuario, ContenidoLibro, Pedido, DetallePedido
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction

def pagina_index(request):
    libros_nuevos = Libro.objects.filter(estado_publicacion='disponible').order_by('-id')[:4]
    contexto = {
        'libros': libros_nuevos,
    }
    return render(request, 'index.html', contexto)

def pagina_proximos(request):
    ebooks_proximos = Libro.objects.filter(estado_publicacion='proximamente', formato='ebook').order_by('fecha_lanzamiento')
    audiobooks_proximos = Libro.objects.filter(estado_publicacion='proximamente', formato='audiobook').order_by('fecha_lanzamiento')
    contexto = {
        'ebooks': ebooks_proximos,
        'audiobooks': audiobooks_proximos,
    }
    return render(request, 'proximos.html', contexto)

def pagina_bookstore(request):
    genero_id = request.GET.get('genero_id')
    
    if genero_id:
        libros_disponibles = Libro.objects.filter(estado_publicacion='disponible', generos__id=genero_id).order_by('-id')
        try:
            genero_id = int(genero_id)
        except ValueError:
            genero_id = None
    else:
        libros_disponibles = Libro.objects.filter(estado_publicacion='disponible').order_by('-id')

    generos = Genero.objects.all()
    libros_adquiridos_ids = []
    
    if request.user.is_authenticated:
        libros_adquiridos_ids = BibliotecaUsuario.objects.filter(usuario=request.user).values_list('libro__id', flat=True)
        
    contexto = {
        'libros': libros_disponibles,
        'generos': generos,
        'libros_adquiridos_ids': libros_adquiridos_ids,
        'genero_id_activo': genero_id
    }
    return render(request, 'bookstore.html', contexto)

def pagina_proximo_detalle(request, id_libro):
    libro = get_object_or_404(Libro, id=id_libro, estado_publicacion='proximamente')
    contexto = {
        'libro': libro,
    }
    return render(request, 'proximo-detalle.html', contexto)

def pagina_libro_detalle(request, id_libro):
    libro = get_object_or_404(Libro, id=id_libro, estado_publicacion='disponible')
    
    ya_adquirido = False
    if request.user.is_authenticated:
        if BibliotecaUsuario.objects.filter(usuario=request.user, libro=libro).exists():
            ya_adquirido = True
            
    contexto = {
        'libro': libro,
        'ya_adquirido': ya_adquirido,
    }
    return render(request, 'libro_detalle.html', contexto)

def pagina_login(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya has iniciado sesión.")
        return redirect('mis_libros')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        contrasena = request.POST.get('password')
        usuario = authenticate(request, username=email, password=contrasena)
        if usuario is not None:
            login(request, usuario)
            return redirect('mis_libros')
        else:
            messages.error(request, 'Correo o contraseña incorrectos.')
            return render(request, 'login.html')
    return render(request, 'login.html')

def pagina_registro(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya tienes una cuenta y has iniciado sesión.")
        return redirect('mis_libros')
    
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo')
        email = request.POST.get('email')
        contrasena = request.POST.get('password')
        confirm_contrasena = request.POST.get('confirm_password')
        if contrasena != confirm_contrasena:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'registro.html')
        if User.objects.filter(username=email).exists():
            messages.error(request, 'El correo electrónico ya está registrado.')
            return render(request, 'registro.html')
        usuario = User.objects.create_user(username=email, email=email, password=contrasena)
        usuario.first_name = nombre_completo 
        usuario.save()
        login(request, usuario)
        return redirect('index')
    return render(request, 'registro.html')

def pagina_logout(request):
    logout(request)
    return redirect('index')

@login_required
def pagina_cuenta(request):
    conteo_libros = BibliotecaUsuario.objects.filter(usuario=request.user).count()
    contexto = {
        'conteo_libros': conteo_libros,
    }
    return render(request, 'cuenta.html', contexto)

@login_required
def pagina_mis_libros(request):
    biblioteca = BibliotecaUsuario.objects.filter(usuario=request.user)
    ids_libros_usuario = biblioteca.values_list('libro__id', flat=True)
    ebooks = Libro.objects.filter(id__in=ids_libros_usuario, formato='ebook')
    audiobooks = Libro.objects.filter(id__in=ids_libros_usuario, formato='audiobook')
    contexto = {
        'ebooks': ebooks,
        'audiobooks': audiobooks,
    }
    return render(request, 'mis-libros.html', contexto)

@login_required
def pagina_leer_libro(request, id_libro, pagina):
    libro = get_object_or_404(Libro, id=id_libro)
    
    contexto = {
        'libro': libro,
        'pagina_actual': None,
        'pista_audio': None,
        'pagina_num': 1,
        'total_paginas': 0,
    }

    if libro.formato == 'ebook':
        contenido = ContenidoLibro.objects.filter(libro=libro, tipo_contenido='imagen').order_by('orden')
        total_paginas = contenido.count()

        try:
            pagina_num = int(pagina)
        except (ValueError, TypeError):
            pagina_num = 1

        if pagina_num < 1:
            pagina_num = 1
        elif pagina_num > total_paginas and total_paginas > 0:
            pagina_num = total_paginas
        elif total_paginas == 0:
            pagina_num = 1

        if total_paginas > 0:
            contexto['pagina_actual'] = contenido[pagina_num-1]
        
        contexto['pagina_num'] = pagina_num
        contexto['total_paginas'] = total_paginas

    elif libro.formato == 'audiobook':
        pista = ContenidoLibro.objects.filter(libro=libro, tipo_contenido='audio').first()
        contexto['pista_audio'] = pista
        
    return render(request, 'leer-libro.html', contexto)

@login_required
def pagina_compra(request, id_libro):
    libro = get_object_or_404(Libro, id=id_libro)
    if BibliotecaUsuario.objects.filter(usuario=request.user, libro=libro).exists():
        messages.info(request, '¡Ya posees este libro!')
        return redirect('libro_detalle', id_libro=id_libro)
    contexto = {
        'libro': libro,
    }
    return render(request, 'compra.html', contexto)

@login_required
@transaction.atomic
def procesar_compra(request, id_libro):
    if request.method == 'POST':
        libro = get_object_or_404(Libro, id=id_libro)
        usuario = request.user
        if BibliotecaUsuario.objects.filter(usuario=usuario, libro=libro).exists():
            messages.error(request, 'Ya has comprado este libro.')
            return redirect('mis_libros')
        try:
            nuevo_pedido = Pedido.objects.create(usuario=usuario, total_pagado=libro.precio, estado_pago='completado')
            DetallePedido.objects.create(pedido=nuevo_pedido, libro=libro, precio_compra=libro.precio)
            BibliotecaUsuario.objects.create(usuario=usuario, libro=libro)
            messages.success(request, f"¡Compra exitosa! '{libro.titulo}' ha sido añadido a tu biblioteca.")
            return redirect('mis_libros')
        except Exception as e:
            messages.error(request, f'Hubo un error al procesar tu compra: {e}')
            return redirect('compra', id_libro=id_libro)
    return redirect('index')