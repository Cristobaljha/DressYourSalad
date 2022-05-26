from django.shortcuts import render, redirect
from .models import Bowl, Pedido, Carrito 
from .forms import BowlForm, PedidoForm, UserRegisterForm, BoletaForm
from django.contrib import messages
from django.contrib.auth.models import User
import pandas as pd 
import numpy as np

from django.db.models import Max, Sum

IdCarrito = 1
Carro_Activo = 1
# Create your views here.

def carritoActivo(user):
	global IdCarrito, Carro_Activo
	IdCarrito = Pedido.objects.all().aggregate(Max('id_carrito'))
	Carro_Activo = Pedido.objects.all().filter(pagado=False).filter(user_id=user).filter(reservado=0).aggregate(Max('id_carrito'))

def index(request):
    try:
        user = User.objects.get(username=request.user)
        if not user.is_superuser:
            return render(request, 'index.html', {'user_id':user.id, 'nombre_user':user.username, 'superuser':user.is_superuser})
        else:
            return render(request, 'admin/dashboard.html')
    except:
            return render(request, 'index.html', {'user_id':0, 'nombre_user':''})

def dashboard(request):
    
    #bowls= Bowl.objects.all()
    bowlsBD = Bowl.objects.values_list('nom_Bowl', flat=True).order_by('cod_Bowl')
    labelsBowls = list(bowlsBD)

    DataBowls = []

    queryset = Pedido.objects.values('bowl_id').annotate(venta=Sum('cantidad')).filter(pagado=True).order_by('bowl_id')
    
    for entry in queryset:
        DataBowls.append(entry['venta'])
    
    return render(request, 'admin/dashboard.html', {'labelsBowls':labelsBowls, 'DataBowls':DataBowls})


def pago(request):   
    bowls= Bowl.objects.all()
    datos ={
        'bowls': bowls      
    }
    return render(request, 'pago.html', datos)

def form_ver(request):
    try:
        user = User.objects.get(username=request.user)
        if user.is_superuser:
            bowls = Bowl.objects.all()
            #bowls = Pedido.objects.select_related().all()
            return render(request, 'admin/form_ver.html', {'bowls':bowls})
        else:
            return render(request, 'index.html', {'user_id':user.id, 'nombre_user':user.username, 'superuser':user.is_superuser})
    except:
        return render(request, 'index.html', {'user_id':0, 'nombre_user':''})

def form_crear(request):
    if request.method=='POST': 
        bowl_form = BowlForm(request.POST)
        if bowl_form.is_valid():
            bowl_form.save()
            return redirect('form_ver')
    else:
       bowl_form= BowlForm()
    return render(request, 'admin/form_crear.html', {'bowl_form': bowl_form})

def form_modificar(request,id):
    bowl = Bowl.objects.get(cod_Bowl=id)

    datos ={
        'form': BowlForm(instance=bowl)
    }
    if request.method == 'POST': 
        formulario = BowlForm(data=request.POST, instance = bowl)
        if formulario.is_valid: 
            formulario.save()
            return redirect('form_ver')
    return render(request, 'admin/form_modificar.html', datos)

def form_eliminar(request,id):
    bowl = Bowl.objects.get(cod_Bowl=id)
    bowl.delete()
    return redirect('form_ver')

def form_bowls(request):

    bowls2 = Bowl.objects.select_related().all() 
    return render(request, 'admin/form_pedido.html', {'bowls2':bowls2})

def seguir_comprando(request, id):
    
    user = User.objects.get(username=request.user)
    bowls2 = Bowl.objects.select_related().all() 
    #return render(request, 'pedido/form_pedido.html', {'bowls2':bowls2, 'ped_form':ped_form, 'user':user})
    return redirect('../form_pedido', {'bowls2':bowls2, 'user':user, 'IdCarrito':id})

def ver_carrito(request, id):
    user = User.objects.get(username=request.user)
    pedidos = Pedido.objects.select_related().all().order_by('-cod_ped').filter(id_carrito=id)
    total = Pedido.objects.all().filter(id_carrito=id).aggregate(Sum('precio'))
    return render(request, 'pedido/form_carrito.html', {'pedidos':pedidos, 'total':total, 'IdCarrito':id, 'user_id':user.id, 'nombre_user': user.username})

def form_pedido(request):
    try:
        user = User.objects.get(username=request.user)
        carritoActivo(user)
        #Cuando no existe ningun carrito inicializamos.
        if(IdCarrito['id_carrito__max']  is None):
            Carro_Activo['id_carrito__max'] = 100

        else:
            #Si hay carrito activo   
            if(Carro_Activo['id_carrito__max']  is None):
                Carro_Activo['id_carrito__max'] = IdCarrito['id_carrito__max'] + 1   
        IdCarritoActivo =  Carro_Activo['id_carrito__max']
        items_carrito = Pedido.objects.filter(id_carrito=IdCarritoActivo).count()


        if request.method=='POST':
            ped_form = PedidoForm(request.POST)
            user = User.objects.get(username=request.user)
            
            if ped_form.is_valid():
                bowl = Bowl.objects.get(cod_Bowl=ped_form['bowl'].value())
                bowls2 = Bowl.objects.select_related().all() 

                carritoActivo(user)
                if bowl.cant_Bowl < int(ped_form['cantidad'].value()):
                    #return redirect('form_pedido', error='error')
                    ped_form=PedidoForm()
                    user = User.objects.get(username=request.user)
                    return render(request, 'pedido/form_pedido.html', {'bowls2':bowls2, 'ped_form':ped_form, 'user':user, 'error':True, 'IdCarrito': IdCarritoActivo, 'Id_Bowl': bowl.cod_Bowl})
                else:
                    
                    bowl.cant_Bowl = bowl.cant_Bowl - int(ped_form['cantidad'].value())
                    pedido = Pedido(cantidad=ped_form['cantidad'].value(), bowl_id=ped_form['bowl'].value(), user_id=user.id,precio = (bowl.precio_Bowl*int(ped_form['cantidad'].value())), id_carrito=ped_form['id_carrito'].value())
                    pedido.save()
                    idPed = bowl.save()
                    
                    pedidos = Pedido.objects.select_related().all().order_by('-cod_ped').filter(pagado=False).filter(reservado=0)
                    total = Pedido.objects.all().filter(id_carrito=ped_form['id_carrito'].value()).aggregate(Sum('precio'))
                    
                    pedido3 = Pedido.objects.filter(user_id=user.id).latest('cod_ped')
                    PrecioCarrito= pedido3.precio
                    CantidadCarrito= int(pedido3.cantidad)
                    #(Bowl.precio_Bowl*int(ped_form['cantidad'].value()))
                    items_carrito2 = Pedido.objects.filter(id_carrito=IdCarritoActivo).count()
                    CarritoBD2 = Carrito.objects.filter(id_carrito=IdCarritoActivo).count()
                    

                    if (items_carrito2 > 1 or CarritoBD2 == 1):
                        carrito5 = Carrito.objects.get(id_carrito=IdCarritoActivo)
                        carrito5.precio = carrito5.precio + PrecioCarrito
                        carrito5.cantidad = carrito5.cantidad + CantidadCarrito
                    else:
                        carrito5 = Carrito(id_carrito=IdCarritoActivo, precio = PrecioCarrito, cantidad=CantidadCarrito,  user_id=user.id)

                    carrito5.save()

                    return render(request, 'pedido/form_carrito.html', {'pedidos':pedidos, 'total':total, 'IdCarrito':ped_form['id_carrito'].value(), 'user_id':user.id, 'nombre_user': user.username})
        else:
            ped_form=PedidoForm()

            try:
                
                bowls2 = Bowl.objects.select_related().all()             
                if not user.is_superuser:
                    return render(request, 'pedido/form_pedido.html', {'bowls2':bowls2 ,'ped_form':ped_form, 'user':user,  'error':False, 'IdCarrito':IdCarritoActivo, 'Id_Bowl':0, 'items_carrito':items_carrito, 'user_id':user.id, 'nombre_user': user.username})
                else:
                    return render(request, 'index.html', {'user_id':user.id, 'nombre_user':user.username, 'superuser':user.is_superuser})
            except:
                return redirect('accounts/login')
    except:
        return render(request, 'index.html', {'user_id':0, 'nombre_user':''})

def form_eliminar_carrito (request,id,id2):
    
    pedido = Pedido.objects.get(cod_ped=id) 
    bowl = Bowl.objects.get(cod_Bowl=pedido.bowl_id)
    bowl.cant_Bowl = bowl.cant_Bowl + int(pedido.cantidad)
    pedido.delete()
    bowl.save() 
    
    carrito5 = Carrito.objects.get(id_carrito=id2)
    carrito5.precio = carrito5.precio - pedido.precio
    carrito5.cantidad = carrito5.cantidad - int(pedido.cantidad)
    
    carrito5.save()


    user = User.objects.get(username=request.user)

    pedidos = Pedido.objects.select_related().all().order_by('-cod_ped').filter(pagado=False).filter(reservado=0)
    total = Pedido.objects.all().filter(id_carrito=id2).aggregate(Sum('precio'))
    return render(request, 'pedido/form_carrito.html', {'pedidos':pedidos, 'total':total, 'IdCarrito':id2, 'user_id':user.id, 'nombre_user': user.username})    


def registro(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('index')
	else:
		form = UserRegisterForm()

	context = { 'form' : form } 
	return render(request, 'loginadmin/registro.html', context)

def form_ver_pedidos(request): 

    pedidos = Carrito.objects.select_related().all().order_by('-id_carrito').filter(pagado=False)
    return render(request, 'admin/form_ver_pedidos.html', {'pedidos':pedidos})

def form_ver_pagados(request):
    pedidos = Carrito.objects.select_related().all().order_by('-id_carrito').filter(pagado=True).filter(entregado=False)
    return render(request, 'admin/form_ver_pagados.html', {'pedidos':pedidos})

def form_entregado(request, id):
      #pedido = Pedido.objects.get(id_carrito=id)
    Pedido.objects.filter(id_carrito=id).update(entregado=True)
    #pedido.save()

    CarritoBD = Carrito.objects.get(id_carrito=id)
    CarritoBD.entregado = True
    CarritoBD.save()

    return redirect('form_ver_pagados')

def form_noentregado(request, id):
    pedido = Pedido.objects.get(cod_ped=id)
    pedido.entregado = False
    pedido.save()

    return redirect('form_ver_pagados')

def form_pagado(request, id):
    #pedido = Pedido.objects.get(id_carrito=id)
    Pedido.objects.filter(id_carrito=id).update(pagado=True)
    #pedido.save()

    CarritoBD = Carrito.objects.get(id_carrito=id)
    CarritoBD.pagado = True
    CarritoBD.save()

    return redirect('form_ver_pedidos')

def form_nopagado(request, id):
    pedido = Pedido.objects.get(cod_ped=id)
    pedido.pagado = False
    pedido.save()

    return redirect('form_ver_pedidos')

def reservar_carrito(request, id):
    Pedido.objects.filter(id_carrito=id).update(reservado=1)
    total = Pedido.objects.all().filter(id_carrito=id).aggregate(Sum('precio'))

    return render(request, 'pago.html', {'IdCarrito':id, 'total':total})

def form_boleta2(request,id):
    pedido = Pedido.objects.get(cod_ped=id)
    
    datos ={
        'form': BoletaForm(instance=pedido)
    }
    if request.method == 'POST': 
        
        formulario = BoletaForm(data=request.POST, instance = pedido)
        if formulario.is_valid: 
            formulario.save()
            return redirect('form_ver_pagados')
    
    return render(request, 'admin/form_modificar_pedidos.html', datos)

def form_boleta(request,id):
    carrito = Carrito.objects.get(id_carrito=id)
    
    datos ={
        'form': BoletaForm(instance=carrito)
    }
    if request.method == 'POST': 
        
        formulario = BoletaForm(data=request.POST, instance = carrito)
        if formulario.is_valid: 
            formulario.save()
            return redirect('form_ver_pedidos')
    
    return render(request, 'admin/form_modificar_pedidos.html', datos)

