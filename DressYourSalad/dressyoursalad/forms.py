from django import forms
from django.forms import ModelForm
from django.forms.models import ModelChoiceField
from django.forms.widgets import Widget
from .models import Bowl


class BowlForm(forms.ModelForm):
    
    class Meta:
        model = Bowl
        fields = ['cod_Bowl', 'nom_Bowl', 'precio_Bowl', 'descripcion_Bowl', 'cant_Bowl', 'estado_stock']
        labels ={
            'cod_Bowl': 'Código', 
            'nom_Bowl': 'Nombre', 
            'precio_Bowl': 'Precio', 
            'descripcion_Bowl': 'Descripcion',
            'cant_Bowl': 'Cantidad',
            'estado_stock': 'Estado'
        }
        widgets={
            'cod_Bowl': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ingrese codigo', 
                    'id': 'cod_Bowl'
                }
            ), 
            'nom_Bowl': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ingrese nombre', 
                    'id': 'nom_Bowl'
                }
            ), 
            'precio_Bowl': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ingrese precio', 
                    'id': 'precio_Bowl'
                }
            ), 
            'descripcion_Bowl': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese descripción', 
                    'id': 'descripcion_Bowl',
                }
            ),
            'estado_stock': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese estado', 
                    'id': 'estado_stock',
                }
            )

        }
