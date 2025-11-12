from django import forms
from django.contrib.auth.models import User
from tienda.models import Libro, Genero, Autor

class LibroForm(forms.ModelForm):
    
    generos = forms.ModelMultipleChoiceField(
        queryset=Genero.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    autores = forms.ModelMultipleChoiceField(
        queryset=Autor.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Libro
        fields = [
            'titulo', 
            'descripcion', 
            'precio', 
            'portada', 
            'estado_publicacion', 
            'formato',
            'fecha_lanzamiento',
            'duracion_minutos',
            'generos',
            'autores'
        ]
        
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'portada': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'estado_publicacion': forms.Select(attrs={'class': 'form-control'}),
            'formato': forms.Select(attrs={'class': 'form-control'}),
            'fecha_lanzamiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duracion_minutos': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'is_staff', 'is_superuser']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nombre_genero', 'descripcion_genero']
        widgets = {
            'nombre_genero': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_genero': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre_autor', 'biografia', 'foto']
        widgets = {
            'nombre_autor': forms.TextInput(attrs={'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }