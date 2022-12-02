from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse

from django.views.generic.list import ListView
from django.views import generic

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from gestor.models import Producto
from gestor.forms import ProductoForm


def registrar(request):
    
    if request.method == 'GET':
        return render(request, 'registrar.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            # registrando usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                if not user is None: 
                    user.save()
                    login(request, user)
                    return redirect('home')
            except IntegrityError:
                return render(request, 'registrar.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya esta registrado'
                })
        else:
            return render(request, 'registrar.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coindicen'
        })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html',{
        'form': AuthenticationForm
        })
    else:
        
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o Contraseña Invalido'
            })
        else:
            login(request, user)
            return redirect('home')  
        
# Create your views here.
def index(request):
    ultimos_productos = list(Producto.objects.all())[-6:]
    productos_a_vencer = list(
        Producto.objects.all().order_by('fechaVnto'))[-6:]
    context = {
        'ultimos_productos': ultimos_productos,
        'productos_a_vencer': productos_a_vencer,
    }
    return render(request, 'index.html', context)


class ProductoListView(generic.ListView):
    # model = Producto
    # context_object_name = 'productos'
    # queryset = Producto.objects.all()
    # template_name='productos.html'
    @login_required(login_url='/signin/')
    def producto_delete(request, pk):
        prod = Producto.objects.get(pk=pk)
        prod.delete()
        return redirect('home')

    def Buscar(request):

        productos = Producto.objects.all()
        busqueda = request.GET.get("myInput")

        if busqueda:
            productos = Producto.objects.filter(
                Q(marca__icontains=busqueda) |
                Q(producto__icontains=busqueda) |
                Q(codStock__icontains=busqueda)
            )
        return render(request, 'productos.html', {'productos': productos})


class VencimientoListView(generic.ListView):
    # model = Producto
    # context_object_name = 'productos'
    # queryset = Producto.objects.all()
    # template_name='productos.html'
    @login_required(login_url='/signin/')
    def producto_delete(request, pk):
        prod = Producto.objects.get(pk=pk)
        prod.delete()
        return redirect('home')

    def Buscar(request):

        productos = Producto.objects.all()
        busqueda = request.GET.get("myInput")

        if busqueda:
            productos = Producto.objects.filter(
                Q(marca__icontains=busqueda) |
                Q(producto__icontains=busqueda) |
                Q(codStock__icontains=busqueda)
            )
        return render(request, 'vencimientos.html', {'productos': productos})

@login_required(login_url='/signin/')
def configurar(request):
    return render(request, 'configurar.html')

@login_required(login_url='/signin/')
def producto_new(request):
    if request.method == 'POST':
        formulario = ProductoForm(request.POST)
        if formulario.is_valid():
            producto = formulario.save(commit=False)
            producto.marca = formulario.cleaned_data['marca']
            producto.producto = formulario.cleaned_data['producto']
            producto.tipo = formulario.cleaned_data['tipo']
            producto.fechaIngreso = formulario.cleaned_data['fechaIngreso']
            producto.fechaVnto = formulario.cleaned_data['fechaVnto']
            producto.stockIng = formulario.cleaned_data['stockIng']
            producto.stockDisp = formulario.cleaned_data['stockIng']
            producto.codStock = formulario.cleaned_data['codStock']
            producto.save()

            return redirect('home')
        else:
            return render(request, 'producto_new.html', {'formulario': formulario})
    else:
        formulario = ProductoForm()
    return render(request, 'producto_new.html', {'formulario': formulario})

@login_required(login_url='/signin/')
def producto_update(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == "POST":
        formulario = ProductoForm(request.POST, instance=producto)
        if formulario.is_valid():
            producto = formulario.save(commit=False)
            producto.marca = formulario.cleaned_data['marca']
            producto.producto = formulario.cleaned_data['producto']
            producto.tipo = formulario.cleaned_data['tipo']
            producto.fechaIngreso = formulario.cleaned_data['fechaIngreso']
            producto.fechaVnto = formulario.cleaned_data['fechaVnto']
            producto.stockIng = formulario.cleaned_data['stockIng']
            producto.stockDisp = formulario.cleaned_data['stockIng']
            producto.codStock = formulario.cleaned_data['codStock']
            producto.save()
            return redirect('home')
    else:
        formulario = ProductoForm(instance=producto)

    return render(request, 'producto_new.html', {'formulario': formulario})
