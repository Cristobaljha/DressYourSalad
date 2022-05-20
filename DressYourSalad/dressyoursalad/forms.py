from django import forms
from django.forms import ModelForm
from django.forms.models import ModelChoiceField
from django.forms.widgets import Widget
from .models import Bowl, Pedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BowlForm(forms.ModelForm):
    
    class Meta:
        model = Bowl
        fields = ['cod_Bowl', 'nom_Bowl', 'precio_Bowl', 'descripcion_Bowl', 'cant_Bowl']
        labels ={
            'cod_Bowl': 'Código', 
            'nom_Bowl': 'Nombre', 
            'precio_Bowl': 'Precio', 
            'descripcion_Bowl': 'Descripcion',
            'cant_Bowl': 'Cantidad',
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
            )

        }

class PedidoForm(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['cantidad', 'bowl']
        labels ={
            'cantidad': 'Cantidad', 
            'bowl': 'Elige tu bowl'            
        }
        widgets={
            
            'cantidad': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'id': 'cantidad'
                }
            ),
            'bowl': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id': 'bowl',
                }
            )

        }


class ModificarPedidoForm(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['pagado']
        labels ={       
        
            'pagado': 'No pagado: False - Pagado: True' 
        }           
        
        widgets={
            
            'pagado': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'id': 'pagado',
                }
            )
        }

#configuracion del page registro

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	password1 = forms.CharField(label='Contraseña: (Mínimo 8 caracteres)', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirma Contraseña', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
		help_texts = {k:"" for k in fields }