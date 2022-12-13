import calendar
import datetime
import os

from datetime import date, timedelta

from importlib.abc import Finder

from django.db import IntegrityError
from django.db.models import Q

from django.shortcuts import get_object_or_404, redirect, render

from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404


from django.urls import reverse, reverse_lazy

from django.views.generic.list import ListView
from django.views import generic

from django.utils.safestring import mark_safe

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator

from gestor.models import EventMember, Evento, Producto
from gestor.forms import AddMemberForm, EventForm, ProductoForm
from gestor.utils import Calendar

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
    ultimos_productos = list(Producto.objects.all())[-3:]
    productos_a_vencer = list(
        Producto.objects.all().order_by('fechaVnto'))[-3:]
    context = {
        'ultimos_productos': ultimos_productos,
        'productos_a_vencer': productos_a_vencer,
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

#LISTA DE EVENTOS
class AllEventsListView(ListView):
    """ All event list views """

    template_name = "events_list.html"
    model = Evento

    def get_queryset(self):
        return Evento.objects.get_all_events(user=self.request.user)


class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "events_list.html"
    model = Evento

    def get_queryset(self):
        return Evento.objects.get_running_events(user=self.request.user)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "accounts:signin"
    model = Evento
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


@login_required(login_url="signup")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["titulo"]
        description = form.cleaned_data["descripcion"]
        start_time = form.cleaned_data["tiempo_inicio"]
        end_time = form.cleaned_data["tiempo_fin"]
        Evento.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    model = Evento
    fields = ["titulo", "descripcion", "tiempo_inicio", "tiempo_fin"]
    template_name = "event.html"


@login_required(login_url="signup")
def event_details(request, event_id):
    event = Evento.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Evento.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["usuario"]
                EventMember.objects.create(event=event, user=user)
                return redirect("calendar")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendar")


class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "signin"
    template_name = "calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = Evento.objects.get_all_events(user=request.user)
        events_month = Evento.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.titulo,
                    "start": event.tiempo_inicio.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.tiempo_fin.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)