from django.db import models

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
    codBulto = models.CharField('Codigo de Bulto',max_length=13,help_text="Codigo que figura en el bulto ",blank=True) # LOS FARDOS EN GRAL CONTIENEN UN CODIGO DEL MISMO
    imagen = models.ImageField(upload_to='img/',null=True)


    def __str__(self):
        return 'Marca: %s -- Tipo: %s' % (self.marca, self.tipo)

    def prod_id (self):
        return self.pk

    class Meta:
        ordering = ['fechaVnto']