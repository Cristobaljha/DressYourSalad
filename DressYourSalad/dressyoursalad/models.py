from django.db import models

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
