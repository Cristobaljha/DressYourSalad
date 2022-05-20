from django.db import models
from django.utils.timezone import datetime
from django.contrib.auth.models import User

# Create your models here.

#Modelo para bowl

class Bowl (models.Model):
    cod_Bowl = models.CharField(max_length=10,primary_key=True, verbose_name='cod Bowl')
    nom_Bowl = models.CharField(max_length=25,verbose_name='Nombre Bowl')
    precio_Bowl = models.IntegerField(verbose_name='Precio Bowl')
    descripcion_Bowl = models.CharField(max_length=50, verbose_name='descripcion Bowl')
    cant_Bowl = models.IntegerField(verbose_name='Cantidad de Bowl')
    estado_stock = models.CharField(max_length=10, verbose_name='Estado Bowl')

    def __str__(self):
        return self.cod_Bowl

class Pedido (models.Model):
    cod_ped = models.AutoField(primary_key=True, editable=False)
    fecha_ped = models.DateTimeField(default=datetime.now, editable=False)
    cantidad = models.CharField(max_length=25,verbose_name='Cantidad Bowl')
    pagado=models.BooleanField(default=False)
    bowl=models.ForeignKey(Bowl, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __int__(self):
        return self.cod_ped