from django.shortcuts import render, redirect
from .models import Bowl 
from .forms import BowlForm

# Create your views here.

def index(request):
    return render(request, 'index.html')


def carrito(request):
    bowls= Bowl.objects.all()
    
    datos ={
        'bowls': bowls
    }
    
    return render(request, 'carrito.html', datos)



def pago(request):
    #accediendo al objeto que contiene los datos de la base 
    #el metodo all traerá todos los bowls que están en la tabla
    bowls= Bowl.objects.all()
    #ahora crearemos una variable que le pase los datos del bowl al template 
    datos ={
        'bowls': bowls
    }
    #ahora lo agregamos para que se envíe al template
    return render(request, 'pago.html', datos)

def form_ver(request):
    bowls = Bowl.objects.all()
    return render(request, 'admin/form_ver.html', {'bowls':bowls})

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


def registro(request):

    return render(request, 'logincli/registro.html')



def login(request):

    return render(request, 'logincli/login.html')
