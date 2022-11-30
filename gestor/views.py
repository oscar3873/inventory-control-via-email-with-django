from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.list import ListView
from gestor.forms import ProductoForm
from django.views import generic
from django.db.models import Q

from gestor.models import Producto

# Create your views here.
def index(request):
    ultimos_productos = list(Producto.objects.all())[-6:]
    productos_a_vencer = list(Producto.objects.all().order_by('fechaVnto'))[-6:]
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

    def producto_delete(request, pk):
        prod = Producto.objects.get(pk=pk)
        prod.delete()
        return redirect('home')

    def Buscar(request):

        productos = Producto.objects.all()
        busqueda= request.GET.get("myInput")
        
        if busqueda :
            productos = Producto.objects.filter(
                Q(marca__icontains = busqueda) |
                Q(producto__icontains = busqueda) |
                Q(codStock__icontains = busqueda)
            )
        return render(request, 'productos.html', {'productos' : productos} )

def configurar(request):
    return render(request, 'configurar.html')

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
            return render(request, 'producto_new.html',{'formulario':formulario})
    else:
        formulario = ProductoForm()
    return render(request, 'producto_new.html', {'formulario': formulario})

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
    
    return render(request, 'producto_new.html', {'formulario':formulario})