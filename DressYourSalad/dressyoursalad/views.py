from django.shortcuts import render, redirect
from .models import Bowl, Pedido, Carrito 
from .forms import BowlForm, PedidoForm, UserRegisterForm, BoletaForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connection
import pandas as pd 
import numpy as np

from django.db.models import Max, Sum

IdCarrito = 1
Carro_Activo = 1
# Create your views here.

def carritoActivo(user):
	global IdCarrito, Carro_Activo
	IdCarrito = Pedido.objects.all().aggregate(Max('id_carrito'))
	Carro_Activo = Pedido.objects.all().filter(pagado=False).filter(user_id=user.id).filter(reservado=0).aggregate(Max('id_carrito'))

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
    
    labelsBowls1=[]
    with connection.cursor() as cursor:
        cursor.execute("Select  nom_Bowl, sum(cantidad) from dressyoursalad_pedido,  dressyoursalad_bowl where pagado = 1 and cod_bowl = bowl_id group by bowl_id, nom_Bowl order by 2 desc  FETCH FIRST 4 ROWS ONLY")
        cursor1 = cursor.fetchall()
        for row1 in cursor1:
            labelsBowls1.append(list(row1))
    labelsBowls = list(labelsBowls1)

    DataBowls1=[]
    with connection.cursor() as cursor:
        cursor.execute("Select   sum(cantidad) from dressyoursalad_pedido where pagado = 1 group by bowl_id  order by 1 desc  FETCH FIRST 4 ROWS ONLY ")
        cursor2 = cursor.fetchall()
        for row2 in cursor2:
            DataBowls1.append(list(row2))
    DataBowls = list(DataBowls1)

    labelsClientes1=[]
    with connection.cursor() as cursor:
        cursor.execute("Select  username, count(*) FROm dressyoursalad_carrito,  auth_user where pagado = 1 and user_id = auth_user.id group by user_id, username order by 2 desc  FETCH FIRST 3 ROWS ONLY")
        cursor3 = cursor.fetchall()
        for row3 in cursor3:
            labelsClientes1.append(list(row3))
    labelsClientes = list(labelsClientes1)

    DataClientes2=[]
    with connection.cursor() as cursor:
        cursor.execute("Select   count(*) FROm dressyoursalad_carrito,  auth_user where pagado = 1 and user_id = auth_user.id group by user_id, username order by 1 desc  FETCH FIRST 3 ROWS ONLY")
        cursor4 = cursor.fetchall()
        for row4 in cursor4:
            DataClientes2.append(list(row4))
    DataClientes = list(DataClientes2)

    DataVentas1=[]
    with connection.cursor() as cursor:
        cursor.execute("Select  to_char(TO_DATE(TRUNC(fecha_ped))), count(*) from dressyoursalad_carrito where pagado = 1 group by trunc(fecha_ped) order by 2 desc  FETCH FIRST 3 ROWS ONLY")
        cursor5 = cursor.fetchall()
        for row5 in cursor5:
            DataVentas1.append(list(row5))
    DataVentas2 = list(DataVentas1)    
    LabelsVentas = []
    DataVentas = []
    for x,y in  DataVentas2:
       LabelsVentas.append(x.replace(' 00:00:00','')) 
       DataVentas.append(y) 
       
   
    return render(request, 'admin/dashboard.html', {'labelsBowls':labelsBowls, 'DataBowls':DataBowls, 'labelsClientes':labelsClientes,'DataClientes':DataClientes,'LabelsVentas':LabelsVentas, 'DataVentas':DataVentas})


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
                    bowl.save()
                    
                    pedidos = Pedido.objects.select_related().all().filter(id_carrito=ped_form['id_carrito'].value()).filter(pagado=False).filter(reservado=0).order_by('-cod_ped')
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

    pedidos = Pedido.objects.select_related().all().filter(id_carrito=id2).filter(pagado=False).filter(reservado=0).order_by('-cod_ped')
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

def form_reportevtas(request):   

    DataVentas1=[]
    with connection.cursor() as cursor:
        cursor.execute("Select  to_char(TO_DATE(TRUNC(fecha_ped))) from dressyoursalad_carrito where pagado = 1 group by trunc(fecha_ped) order by 1 desc")
        cursor5 = cursor.fetchall()
        for row5 in cursor5:
            DataVentas1.append(list(row5))
    DataVentas2 = list(DataVentas1)    
    FechaVtas = []
    for x in  DataVentas2:
       txt = x[0]     
       spl = txt.split(" ")
       txt2 = spl[0]
       txt3 = txt2.replace("['","")
       FechaVtas.append(txt3)


    pedidos = Carrito.objects.select_related().all().order_by('-id_carrito').filter(pagado=True)
    return render(request, 'admin/form_reportevtas.html', {'pedidos':pedidos, 'FechaVtas':FechaVtas})

