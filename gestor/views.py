import datetime
import json
import os

from django.db import IntegrityError
from django.db.models import Q

from django.shortcuts import get_object_or_404, redirect, render

from django.http import Http404

from django.views.generic.list import ListView
from django.views import generic

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator

from gestor.models import Producto
from gestor.forms import ProductoForm

from gestor.utils import insertGoogleCalendar

#REGISTRAR USUARIOS
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

#CERRAR SESION

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
        
# DASHBOARD

def index(request):
    ultimos_productos = list(Producto.objects.all()) [-3:]
    productos_a_vencer = list(Producto.objects.all().order_by('fechaVnto')) [-3:]

    date = datetime.date.today()
    productos_vencidos = 0
    for prod_ven in Producto.objects.all():
        if prod_ven.fechaVnto <= date:
            productos_vencidos = productos_vencidos+1
    
    prod_mes = Producto.objects.all().order_by('fechaIngreso__year','fechaIngreso__month')
    prod_ord_mes =[[], [], [], [], [], [], [], [], [], [], [], []]
    for p_m in prod_mes:
        if p_m.fechaIngreso.year == date.year:  # PRODUCTOS ORDENADOS POR MES DE INGRESO (ASCENDENTE) EN EL AÑO ACTUAL
            prod_ord_mes[p_m.fechaIngreso.month - 1].append(p_m)
    
    prod_mes1 = Producto.objects.all().order_by('fechaIngreso__year','fechaIngreso__month')
    prod_ord_mes1 =[[], [], [], [], [], [], [], [], [], [], [], []]
    for p_m1 in prod_mes1:
        if p_m1.fechaVnto.year == date.year and p_m1.fechaVnto.month <= date.month and p_m1.fechaVnto.day < date.day:  # PRODUCTOS ORDENADOS POR MES DE INGRESO (ASCENDENTE) EN EL AÑO ACTUAL
            prod_ord_mes1[p_m1.fechaVnto.month - 1].append(p_m1)

    productos_all = []
    for p_all in prod_mes:
        if p_all.fechaIngreso.year == date.year:
            productos_all.append(p_all)

    prod_ord_mes_ven = []
    prod_vencidos_all = []
    for p_m_v in prod_mes:
        if p_m_v.fechaVnto <= date:
            prod_vencidos_all.append(p_m_v)     # TODOS LOS PRODUCTOS VENCIDOS HOSTORICOS

        if p_m_v.fechaVnto.year == date.year:  
            prod_ord_mes_ven.append(p_m_v)

    prod_ven_año = []
    for p_v in prod_ord_mes_ven:
        if p_v.fechaVnto <= date:
            prod_ven_año.append(p_v) # TODOS LOS PRODUCTOS VENCIDOS ANUAL


    producots_vencidos = Producto.objects.filter(vencido = True)

    if Producto.objects.all().count():
        porcentaje_ven = round((100*(len(prod_vencidos_all) / Producto.objects.all().count() )),2)
        porcentaje_ven_actual = round((100*(len(prod_ven_año) / len(productos_all))),2)
    else :
        porcentaje_ven = 0
        porcentaje_ven_actual = 0


    cont = 0
    listado = []
    for ind in prod_ord_mes:
        if ind:
            listado.append(len(ind))
        else : 
            listado.append(0)
        cont = cont+1


    cont_ven = 0
    listado_ven = []
    for ind1 in prod_ord_mes1:
        if ind1:
            listado_ven.append(len(ind1))
        else : 
            listado_ven.append(0)
        cont_ven = cont_ven+1

    lista=[]
    lista_stock=[]
    for dex in Producto.objects.all().filter(fechaIngreso__year= date.year):
        lista.append(dex.producto+" (%s)" %dex.marca)
        lista_stock.append(dex.stockIng)
    formulario = ProductoForm()
    context = {
        'formulario':formulario,
        'ultimos_productos': ultimos_productos,
        'productos_a_vencer': productos_a_vencer,  

        'porc_ven' : porcentaje_ven,
        'prod_ven_all' : len(prod_vencidos_all),
        'prod_all' : Producto.objects.all().count(),
        'prod_ven' : len(producots_vencidos),

        'porcentaje_ven_actual' : porcentaje_ven_actual,
        'productos_all_anual': len(productos_all),  # CANTIDAD DE LOS PRODUCTOS INGRESADOS durante el correinte año
        'productos_ven': productos_vencidos,        # CANTIDAD DE LOS PRODUCTOS VENCIDOS EN EL AÑO
        
        #JS
        'listado': json.dumps(listado),             # PRODUCTOS ORDENADOS POR MES DE INGRESO (CANTIDAD POR MES)
        'listado_ven': json.dumps(listado_ven),     # PRODUCTOS ORDENADOS POR MES DE vencidos (CANTIDAD POR MES)
        'lista' : json.dumps(lista),
        'lista_stock' : json.dumps(lista_stock),
    }
    return render(request, 'index.html', context)


#LISTA DE PRODUCTOS
class ProductoListView(generic.ListView):

    def producto_delete(request, pk):
        prod = Producto.objects.get(pk=pk)
        prod.delete()
        return redirect('productos')
    
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
        
#LISTA DE VENCIMIENTOS
class VencimientoListView(generic.ListView):

    def producto_delete(request, pk):
        prod = Producto.objects.get(pk=pk)
        prod.delete()
        return redirect('vencimientos')
        
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


#CONFIGURACION
@login_required(login_url='/signin/')
def configurar(request):
    return render(request, 'configurar.html')


#NUEVO PRODUCTO
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

            for r, d, f in os.walk('.\\media'):
                for files in f:
                    file=os.path.join(files)
                    print( str.lower(producto.producto) ,str.lower(file) )
                    
                    print(os.path.splitext(files)[0]) 
                    if len(str.lower(producto.producto)) <= len(str.lower(os.path.splitext(files)[0])):
                        if str.lower(producto.producto) in str.lower(os.path.splitext(files)[0]):
                            if str.lower(producto.producto)[0] == str.lower(os.path.splitext(files)[0])[0]:
                                producto.imagen = file      
                                break
                        else:
                            producto.imagen = "unknow.png"
                    else: 
                        if str.lower(os.path.splitext(files)[0]) in str.lower(producto.producto):
                            if str.lower(producto.producto)[0] == str.lower(os.path.splitext(files)[0])[0]:
                                producto.imagen = file      
                                break
                        else:
                            producto.imagen = "unknow.png"
                    
            producto.save()
            text = "Vencimiento de {producto} Marca {marca} Codigo {codigo} es el {fecha} 8:00 pm -10:30 pm".format(
                producto = producto.producto,
                marca = producto.marca,
                codigo = producto.codBulto,
                fecha = producto.fechaVnto,
                )
            
            insertGoogleCalendar(text)
            
            return redirect('home')
        else:
            return render(request, 'producto_new.html',{'formulario':formulario})
    else:
        formulario = ProductoForm()
    return render(request, 'producto_new.html', {'formulario': formulario})


#ACTUALIZACION DE PRODUCTO
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

            for r, d, f in os.walk('.\\media'):
                for files in f:
                    file=os.path.join(files)
                    print( str.lower(producto.producto) ,str.lower(file) )
                    print(os.path.splitext(files)[0]) 

                    if len(str.lower(producto.producto)) <= len(str.lower(os.path.splitext(files)[0])):
                        if str.lower(producto.producto) in str.lower(os.path.splitext(files)[0]):
                            if str.lower(producto.producto)[0] == str.lower(os.path.splitext(files)[0])[0]:
                                producto.imagen = file      
                                break
                        else:
                            producto.imagen = "unknow.png"
                    else: 
                        if str.lower(os.path.splitext(files)[0]) in str.lower(producto.producto):
                            if str.lower(producto.producto)[0] == str.lower(os.path.splitext(files)[0])[0]:
                                producto.imagen = file      
                                break
                        else:
                            producto.imagen = "unknow.png"
                    
            producto.save()
            return redirect('home')
    else:
        formulario = ProductoForm(instance=producto)

    return render(request, 'producto_new.html', {'formulario': formulario})


#FUNCION DE BUSQUEDA
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
            

        busqueda = request.GET.get("myInput")
        if busqueda :
            productos = Producto.objects.filter(
                Q(marca__icontains = busqueda) |
                Q(producto__icontains = busqueda) |
                Q(codBulto__icontains = busqueda)
            )
        return render(request, 'productos.html', {'productos' : productos})


############################################ Views para Eventos y Calendario #################################

def calendarView(request):
    
    
    
    return render(request, 'calendar.html')