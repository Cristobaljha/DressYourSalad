from django.shortcuts import render, redirect
from .models import Bowl, Pedido 
from .forms import BowlForm, PedidoForm, UserRegisterForm, ModificarPedidoForm
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    return render(request, 'index.html')

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
            return render(request, 'index.html')
    except:
        return render(request, 'index.html')

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



def form_pedido(request):
    if request.method=='POST':
        ped_form = PedidoForm(request.POST)
        user = User.objects.get(username=request.user)
        if ped_form.is_valid():
            bowl = Bowl.objects.get(cod_Bowl=ped_form['bowl'].value())
            if bowl.cant_Bowl < int(ped_form['cantidad'].value()):
                #return redirect('form_pedido', error='error')
                ped_form=PedidoForm()
                user = User.objects.get(username=request.user)
                return render(request, 'pedido/form_pedido.html', {'ped_form':ped_form, 'user':user, 'error':True})
            else:
                bowl.cant_Bowl = bowl.cant_Bowl - int(ped_form['cantidad'].value())
                ped_form.user_id = user.id
                pedido = Pedido(cantidad=ped_form['cantidad'].value(), bowl_id=ped_form['bowl'].value(), user_id=user.id)
                pedido.save()
                bowl.save()
                return redirect('form_carrito')
    else:
        ped_form=PedidoForm()
        user = User.objects.get(username=request.user)
        return render(request, 'pedido/form_pedido.html', {'ped_form':ped_form, 'user':user, 'error':False})

    
def form_carrito(request):
    #pedidos = Pedido.objects.select_related().all()
    pedidos =  Pedido.objects.select_related().latest('fecha_ped')
    return render(request, 'pedido/form_carrito.html', {'pedidos':pedidos})

def form_eliminar_carrito (request,id):
    pedido = Pedido.objects.get(cod_ped=id) 
    bowl = Bowl.objects.get(cod_Bowl=pedido.bowl_id)
    bowl.cant_Bowl = bowl.cant_Bowl + int(pedido.cantidad)
    pedido.delete()
    bowl.save() 
    return redirect('form_pedido')


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
    pedidos = Pedido.objects.select_related().all()
    return render(request, 'admin/form_ver_pedidos.html', {'pedidos':pedidos})


def form_modificar_pedidos(request,id):
    pedido = Pedido.objects.get(cod_ped=id)

    datos ={
        'form': ModificarPedidoForm(instance=pedido)
    }
    if request.method == 'POST': 
        formulario = ModificarPedidoForm(data=request.POST, instance = pedido)
        if formulario.is_valid: 
            formulario.save()
            return redirect('form_ver_pedidos')
    return render(request, 'admin/form_modificar_pedidos.html', datos)