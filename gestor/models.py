from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Producto(models.Model):
    # CLASE DESTINADA A LOS PRODUCTOS INGRESADOS POR "FARDOS o CAJAS" DE MATERIA PRIMAS
    marca = models.CharField(max_length=50)
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


class Evento(models.Model):
    summary = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    start = models.DateField(blank=False)
    end = models.DateField(blank=False)









EVENT = {
  'summary': 'PRUEBA',
  'description': 'El producto x se vence el dia xx-xx-xxxx',
  'start': {
    'dateTime': '2022-12-14T09:00:00-07:00',
    'timeZone': 'America/Buenos_Aires',
  },
  'end': {
    'dateTime': '2022-12-15T17:00:00-12:00',
    'timeZone': 'America/Buenos_Aires',
  }
}