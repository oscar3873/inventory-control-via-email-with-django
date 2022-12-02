from importlib.abc import Finder
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
import os
from django.views.generic.list import ListView
from django.views import generic

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from gestor.models import Producto
from gestor.forms import ProductoForm

from django.core.paginator import Paginator
from django.http import Http404

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

    def producto_delete(request, pk):
        prod = Producto.objects.get(pk=pk)
        prod.delete()
        return redirect('home')

    
    def list_productos(request):

        productos = Producto.objects.all()
        page = request.GET.get('page', 1)
        busqueda = request.GET.get("myInput")
        
        if busqueda :
            productos = Producto.objects.filter(
                Q(marca__icontains = busqueda) |
                Q(producto__icontains = busqueda) |
                Q(codBulto__icontains = busqueda)
            )
            
        try:
            paginator = Paginator(productos, 6)
            productos = paginator.page(page)
        except:
            raise Http404
        
        context = {
            'productos' : productos,
            'paginator' : paginator,
        }
        
        return render(request, 'productos.html', context)
        
class VencimientoListView(generic.ListView):

    def producto_delete(request, pk):
        prod = Producto.objects.get(pk=pk)
        prod.delete()
        return redirect('home')

    def productos_vencimiento(request):
        productos = Producto.objects.all()
        page = request.GET.get('page', 1)
        busqueda = request.GET.get("myInput")
        
        if busqueda :
            productos = Producto.objects.filter(
                Q(marca__icontains = busqueda) |
                Q(producto__icontains = busqueda) |
                Q(codBulto__icontains = busqueda)
            )
        
        try:
            paginator = Paginator(productos, 5)
            productos = paginator.page(page)
        except:
            raise Http404
        
        context = {
            'productos' : productos,
            'paginator' : paginator,
        }
        
        return render(request, 'vencimientos.html', context)

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
            producto.fechaEnvasado = formulario.cleaned_data['fechaEnvasado']
            producto.stockIng = formulario.cleaned_data['stockIng']
            producto.stockDisp = formulario.cleaned_data['stockIng']
            producto.codBulto = formulario.cleaned_data['codBulto']
            

            # for r, d, f in os.walk('.\\media'):
            #     for files in f:
            #         file=os.path.join(files)
            #         if str.lower(producto.producto) in str.lower(file):
            #             producto.imagen = file        # files es el nombre del archiv
            #             break
                    
            producto.save()

            
            return redirect('home')
        else:
            return render(request, 'producto_new.html',{'formulario':formulario})
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
            producto.codBulto = formulario.cleaned_data['codBulto']

            # for r, d, f in os.walk('.\\media'):
            #     for files in f:
            #         file=os.path.join(files)
            #         if str.lower(producto.producto) in str.lower(file):
            #             producto.imagen = file        # files es el nombre del archiv
            #             break

            producto.save()
            return redirect('home')
    else:
        formulario = ProductoForm(instance=producto)

    return render(request, 'producto_new.html', {'formulario': formulario})


def Buscar(request,busqueda=None):
        productos = Producto.objects.all()
        if busqueda!=None:
            r = request.GET.get("myInput")

            productos = Producto.objects.filter(
                Q(marca__icontains = busqueda) |
                Q(producto__icontains = busqueda) |
                Q(codBulto__icontains = busqueda)
            )

            if r != None:
                productos = productos.filter(
                    Q(marca__icontains = r) |
                    Q(producto__icontains = r) |
                    Q(codBulto__icontains = r)
                )
            context = {
                'productos':productos ,
                'buscado':str.upper(busqueda),
                }
            return render(request, 'producto_esp.html', context)

        busqueda = request.GET.get("myInput")
        if busqueda :
            productos = Producto.objects.filter(
                Q(marca__icontains = busqueda) |
                Q(producto__icontains = busqueda) |
                Q(codBulto__icontains = busqueda)
            )
        return render(request, 'productos.html', {'productos' : productos})
    