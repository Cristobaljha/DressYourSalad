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
        fields = ['cod_Bowl', 'nom_Bowl', 'precio_Bowl', 'descripcion_Bowl', 'cant_Bowl', 'estado_stock']
        labels ={
            'cod_Bowl': 'Código', 
            'nom_Bowl': 'Nombre', 
            'precio_Bowl': 'Precio', 
            'descripcion_Bowl': 'Descripcion',
            'cant_Bowl': 'Cantidad Inicial',
            'estado_stock': 'Imagen',
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
            'precio_Bowl': forms.NumberInput(
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
        
            'cant_Bowl': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese stock', 
                    'id': 'cant_Bowl',
                }
            ), 
            'estado_stock': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese imagen', 
                    'id': 'estado_stock',
                }
            )


        }

class BowlForm2(forms.ModelForm):
    
    class Meta:
        model = Bowl
        fields = ['nom_Bowl', 'precio_Bowl', 'descripcion_Bowl', 'cant_Bowl', 'estado_stock']
        labels ={
            
            'nom_Bowl': 'Nombre', 
            'precio_Bowl': 'Precio', 
            'descripcion_Bowl': 'Descripcion',
            'cant_Bowl': 'Cantidad',
            'estado_stock': 'Imagen',
        }
        widgets={
            
            'nom_Bowl': forms.TextInput(
                attrs={
                    'class': 'form-control', 
                    'placeholder': 'Ingrese nombre', 
                    'id': 'nom_Bowl'
                }
            ), 
            'precio_Bowl': forms.NumberInput(
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
        
            'cant_Bowl': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese stock', 
                    'id': 'cant_Bowl',
                }
            ), 
            'estado_stock': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese imagen', 
                    'id': 'estado_stock',
                }
            )


        }

class PedidoForm(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['cantidad', 'bowl','id_carrito']
        labels ={
            'cantidad': 'Cantidad', 
            'bowl': 'Elige tu bowl'            
        }
        widgets={
            
            'cantidad': forms.NumberInput(
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

class BoletaForm(forms.ModelForm):
    
    class Meta:
        model = Pedido
        fields = ['boleta']
                
        widgets={
            
            'boleta': forms.NumberInput(
                attrs={
                    'class': 'form-control', 
                    'id': 'boleta',
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