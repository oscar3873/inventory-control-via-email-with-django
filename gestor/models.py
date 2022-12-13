from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Producto(models.Model):
    # CLASE DESTINADA A LOS PRODUCTOS INGRESADOS POR "FARDOS o CAJAS" DE MATERIA PRIMAS
    marca = models.CharField(max_length=50,default="Generic")
    producto = models.CharField(max_length=50,help_text="Ingrese materia prima (harina, huevos, levadura, etc.)")
    tipo = models.CharField(max_length=30, help_text="Si corresponde, ejemplo: nombre:harina | tipo:'leudante'/'0000' ")
    fechaIngreso = models.DateField('Fecha de Ingreso',blank=False,help_text="Fecha de Ingreso a la fabrica")
    fechaVnto = models.DateField('Fecha de Vencimiento',blank=False,help_text="Fecha indicada en el envase")
    fechaEnvasado = models.DateField('Fecha de Envasado',blank=False,help_text="Fecha indicada en el envase")
    stockIng= models.PositiveIntegerField('Stock de ingreso',blank=False,help_text="Cantidad por bultos/fardos/cajas")
    stockDisp= models.PositiveIntegerField('Stock disponible',blank=False) # Para los caso de obtener-consumir la materia prima
    codBulto = models.CharField('Codigo de Bulto',max_length=13,help_text="Codigo que figura en el bulto ",blank=False) # LOS FARDOS EN GRAL CONTIENEN UN CODIGO DEL MISMO
   
    imagen = models.ImageField(upload_to='',null=True) # borrar el img/


    def __str__(self):
        return 'Marca: %s -- Tipo: %s' % (self.marca, self.tipo)

    def prod_id (self):
        return self.pk

    class Meta:
        ordering = ['fechaVnto']


class EventAbstract(models.Model):
    # CLASE DESTINADA A LOS EVENTOS PARA EL MANEJADOR DE EVENTOS
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventManager(models.Manager):
    # CLASE DESTINADA A EL MANEJADOR DE EVENTOS
    def get_all_events(self, user):
        events = Evento.objects.filter(usuario=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Evento.objects.filter(
            usuario=user,
            is_active=True,
            is_deleted=False,
            tiempo_fin__gte=datetime.now().date(),
        ).order_by("tiempo_inicio")
        return running_events


class Evento(EventAbstract):
    # CLASE DESTINADA A LOS EVENTOS
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    titulo = models.CharField(max_length=200, unique=True)
    descripcion = models.TextField(help_text="Descricion del evento")
    tiempo_inicio = models.DateTimeField(help_text="tiempo de inicio del evento")
    tiempo_fin = models.DateTimeField(help_text="tiempo en el que finaliza el evento")

    objects = EventManager()

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.titulo} </a>'

class EventMember(EventAbstract):
    """ Event member model """

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, related_name="events")
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_members"
    )

    class Meta:
        unique_together = ["evento", "usuario"]

    def __str__(self):
        return str(self.usuario)