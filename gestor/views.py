from django.shortcuts import render
from django.views.generic.list import ListView

from gestor.models import Producto

# Create your views here.
def index(request):
    return render(request, 'index.html')

class ProductoListView(ListView):
    model = Producto
    paginate_by = 2
    context_object_name = 'libros'
    queryset = Producto.objects.all()
    template_name='productos.html'

def configurar(request):
    return render(request, 'configurar.html')