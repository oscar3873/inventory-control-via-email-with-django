
from django.db import models

class Producto(models.Model):
    # CLASE DESTINADA A LOS PRODUCTOS INGRESADOS POR "FARDOS o CAJAS" DE MATERIA PRIMAS
    marca = models.CharField(max_length=50,default="Generic")
    producto = models.CharField(max_length=50,help_text="Ingrese materia prima (harina, huevos, levadura, etc.)")
    tipo = models.CharField(max_length=30, help_text="Si corresponde, ejemplo: nombre:harina | tipo:'leudante'/'0000' ")
    fechaIngreso = models.DateField('Fecha de Ingreso',blank=False,help_text="Fecha de Ingreso a la fabrica")
    fechaVnto = models.DateField('Fecha de Vencimiento',blank=False,help_text="Fecha que figura en el envase")
    stockIng= models.PositiveIntegerField('Stock de ingreso',blank=False,help_text="cantidad por unidad")
    stockDisp= models.PositiveIntegerField('Stock disponible',blank=False) # Para los caso de obtener-consumir la materia prima
    #codStock = models.CharField('ISBN',max_length=13) # LOS FARDOS EN GRAL CONTIENEN UN CODIGO DEL MISMO

    def __str__(self):
        return 'Marca: %s -- Tipo: %s' % (self.marca, self.tipo)

    def prod_id (self):
        return self.pk

    class Meta:
        ordering = ['fechaVnto']