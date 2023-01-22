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
    vencido = models.BooleanField(default=False)
    entregado = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='',null=True) # borrar el img/


    def __str__(self):
        return 'Marca: %s -- Tipo: %s' % (self.marca, self.tipo)

    def prod_id (self):
        return self.pk

    class Meta:
        ordering = ['fechaIngreso']


class Evento(models.Model):
    summary = models.CharField(max_length=50,null=False)
    description = models.TextField(blank=True,null=False)
    start = models.DateField(blank=False,null=False)
    end = models.DateField(blank=False,null=False)

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









class Empeño(models.Model):
  descripcion = models.CharField(max_length=50,blank=False)
  precio = models.PositiveIntegerField(blank=False)

class Contacto(models.Model):
  TELEFONO = 'Tel.'
  CELULAR = 'Cel.'
  numero = models.PositiveIntegerField(blank=False)
  tipo = models.PositiveIntegerField(
    choices=[
      (TELEFONO, 'Telefono fijo'),
      (CELULAR,'Celular')
    ],
    default= CELULAR,
    blank= False
    )

class Empleado(models.Model):
    nombre = models.CharField(max_length=15,blank=False)
    apellido = models.CharField(max_length=20, blank=False)
    direccion = models.CharField(max_length=50, blank=False)
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE)
    # historial_cobranza = models.ForeignKey()
    # historial_creditos = models.ForeignKey()
    comisiones = models.PositiveBigIntegerField(default=0,blank=False,editable=True)

class Comision(models.Model):
    # registro = models.ForeignKey(Registro,on_delete=models.CASCADE)
    monto = models.PositiveIntegerField(blank=False)
    fecha = models.DateField(default=datetime.today)
    # empleado = models.ForeignKey(Empleado, on_delete=models.RESTRICT)


class Cliente(models.Model):
    # CLASE DESTINADA A LOS PRODUCTOS INGRESADOS POR "FARDOS o CAJAS" DE MATERIA PRIMAS
    nombre = models.CharField(max_length=15,blank=False)
    apellido = models.CharField(max_length=20, blank=False)
    dni = models.PositiveIntegerField(blank=False)
    direccion = models.CharField(max_length=50, blank=False)
    # contacto = models.ForeignKey()
    # credito = models.ForeignKey(Credito,on_delete=models.CASCADE,null=True)
    empeño = models.CharField(max_length=50,blank=False)
    score = models.IntegerField(default=50)

    def __str__(self):
        return '%s,%s' % (self.apellido, self.nombre)
    
class Credito(models.Model):
    monto = models.PositiveIntegerField(blank=False)
    CH = [
        (1,'1'),
        (3,'3'),
        (6,'6'),
        (9,'9'),
        (12,'12'),
    ]
    cuotas = models.IntegerField(choices=CH,default=1)
    fecha_inicio = models.DateField(default=datetime.today)
    fecha_vnto = models.DateField(default=datetime.today)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE,null=True)
    #refinanciamiento 

class Registro(models.Model):
    Emp_Admin = models.ForeignKey(Empleado,on_delete=models.CASCADE,null=True)
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)  

class Ingreso_Egreso(models.Model):
  descripcion = models.CharField(max_length=25,blank=False)
  importe = models.PositiveIntegerField(blank=False)
  fecha = models.DateField(blank=False,default=datetime.today)
  modena = models.CharField(max_length=10,choices=[
      ('Pesos','pesos'),
      ('Dolares','dolares')
    ],
    default='Pesos')
  forma_pago = models.CharField(max_length=15,choices=[
    ('efectivo','Efectivo'),
    ('dolares','Dolares'),
    ('transferencia','Transferencia'),
    ('mercado_pago','Mercado Pago'),]
  )

class Cobro(models.Model):
  monto = models.PositiveIntegerField(blank=False)
  forma_pago = models.CharField(
    max_length=15,
    choices=[
      ('efectivo','Efectivo'),
      ('dolares','Dolares'),
      ('transferencia','Transferencia'),
      ('mercado_pago','Mercado Pago'),
      ]
    )
  fecha = models.DateField(default=datetime.today,blank=False)

