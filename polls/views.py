from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, context
from pyquery import PyQuery
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, User
from .models import Product, tienda, Categoria, Categoriaproducto, Carritodecompra, Pedido, Customer, payudata, Tiendacustom, Ciudad, direccionusuario, estadopedido, Ciudad
from django.views.generic import ListView, CreateView
from .forms import  Registrousuario, TiendaForm, CarritoForm, TiendaForm2, TiendacustomForm, ciudadForm, direccionform, ProductoForm, ProductoForm2
from django.utils.timezone import now
from datetime import datetime  
from django.core import paginator
import hashlib
import mercadopago
import json


def registrousuario(request):
 form=Registrousuario()
 
 return render(request, 'polls/registro.html', {'form':form})


def registrotienda(request):
 form=TiendaForm()
 
 return render(request, 'polls/registrotiendas2.html', {'form':form})
 
def confirmacionregistro(request):
 if request.method == "POST":
    form=Registrousuario(request.POST)
    if form.is_valid():
     form.save()
    return render(request, 'polls/confirmacionregistro.html')
 else:
   return redirect(registrousuario)

@login_required
def confirmacionregistrotienda(request):
 Tienda = tienda.objects.get(usuario=request.user.id)
 categoria = Categoria.objects.get(nombre=Tienda.categoria)
 if request.method == "POST":
    form=TiendaForm(request.POST,request.FILES)
    if form.is_valid():
     form.save()
    return render(request, 'polls/itemstiendas.html',{'Tienda':Tienda,'categoria':categoria})
 else:
   return redirect(registrotienda)


@login_required
def pagomenbresiatienda(request):
 
 Tienda = tienda.objects.get(usuario=request.user.id)
 payu = payudata.objects.get(pk=2)
 a = "1112"
 total = int(Tienda.get_total)
 reference = (a + str(request.user.id))
 currency ="COP"
 text = (str(payu.apikey)+"~"+str(payu.merchantid)+"~"+ str(reference)+"~"+str(total) +"~"+ str(currency))
 textUtf8 = text.encode(encoding='UTF-8')
 hash = hashlib.md5( textUtf8 )
 signature = hash.hexdigest()

 form=TiendaForm2(request.POST, instance=Tienda)
 if request.method == "POST":
    if form.is_valid():
     form.save()
    return render(request, 'polls/Hacerpago.html',{'Tienda':Tienda,'payu':payu,'signature':signature,'reference':reference,'currency':currency,'text':text,'total':total})
 else:
   return redirect(registrotienda)



@login_required
def inicio(request):
  
  model = TiendaForm()
  
  return render(request, 'polls/home.html', {'model':model})


@login_required
def misproductos(request):
  try:
    
   Tienda = tienda.objects.get(usuario=request.user.id)
   context = {'Tienda':Tienda}
  except:
    messages.success(request,"No posees una tienda registrada o activa")
    return redirect('inicio')

  
  context = {'Tienda':Tienda}


  return render(request, 'polls/misproductos.html', context)


@login_required
def mitienda(request):
  form = TiendacustomForm()

  return render(request, 'polls/fondotienda.html', {'form':form})


@login_required
def guadarfondo(request):
  form = TiendacustomForm()
  Tienda = tienda.objects.get(usuario=request.user.id)
  fondo = Tiendacustom.objects.get_or_create(tienda_id=Tienda.nombre)

  if request.method == "POST":
    fondo2 = Tiendacustom.objects.get(tienda_id=Tienda.nombre)
    form=TiendacustomForm(request.POST,request.FILES,instance = fondo2)
    if form.is_valid():
      form.save()
    return render(request, 'polls/fondotienda.html',{'form':form,'Tienda':Tienda,'fondo':fondo})
  

  return render(request, 'polls/fondotienda.html', {'form':form,'fondo':fondo})

@login_required
def mispedidos(request):
  try:
    
    customer = request.user.customer
  except:
    customer, created = Customer.objects.get_or_create(user=request.user) 

  try:
   pedido = Pedido.objects.filter(usuario=request.user.id, completado=True)
   direccion = direccionusuario.objects.get(usuario=request.user.id)
   context = {'pedido':pedido,'direccion':direccion}
  except:
   pedido, created = Pedido.objects.get_or_create(usuario=customer, completado=False)
   context = {'pedido':pedido}
  return render(request, 'polls/mispedidos.html', context)
   
  
@login_required
def hacerpedido(request): 
  try:
    model3 = direccionusuario.objects.get(usuario=request.user.id)
  except:
    return redirect('Midireccion')

  try:
   Tienda = tienda.objects.get(usuario=request.user.id)  
   model = tienda.objects.filter(ciudad=model3.ciudad).values('id','nombre','imagen','categoria','usuario')
   model2=Categoria.objects.values('nombre')
   context={'Tienda':Tienda,'model':model,'model2':model2,'model3':model3}
   return render(request, 'polls/Menunegocios.html',context)
  except:
   model = tienda.objects.filter(ciudad=model3.ciudad).values('id','nombre','imagen','categoria','usuario')
   model2 = Categoria.objects.values('nombre')
   context = {'model':model,'model2':model2,'model3':model3}
   return render(request, 'polls/Menunegocios.html',context)



  
  


def Menuproductos(request):
  idtienda=request.GET['nombre']
  try:
   fondo = Tiendacustom.objects.get(tienda=idtienda)
  except Tiendacustom.DoesNotExist:
   fondo = None
  
  model=tienda.objects.values('id','nombre','imagen','categoria','usuario')
  model2=Product.objects.filter(tiendaid=idtienda).values('id','tiendaid','nombre','imagen','precio','categoria')
  model3=Categoriaproducto.objects.filter(usuario=request.GET['usuario']).values('usuario','nombre')
  
  return render(request, 'polls/Menu_productos.html',{'model':model,'model2':model2,'model3':model3,'fondo':fondo})

def Vistaproducto(request):

  model=tienda.objects.values('id','nombre','imagen','categoria')
  model2=Product.objects.filter(id=request.GET['id']).values('id','nombre','imagen','precio')
 
  return render(request, 'polls/producto.html',{'model':model,'model2':model2})

@login_required
def agregaralcarrito(request):

	product = Product.objects.get(id=request.POST['productoid']) 
  
  
	if request.method == 'POST':
		

		pedido, created = Pedido.objects.get_or_create(usuario=request.user.id, completado=False)
		carritodecompra, created = Carritodecompra.objects.get_or_create(pedido=pedido, productoid=product, tienda=product.tiendaid ,cantidad=request.POST['cantidad'])
		carritodecompra.save()

		return redirect('cart')

	context = {'product':product}
	return redirect('Vistaproducto',context)
   

def cart(request):
  try:
   pedido, created = Pedido.objects.get_or_create(usuario=request.user.id, completado=False)
   direccion = direccionusuario.objects.get(usuario=request.user.id)
   context = {'pedido':pedido,'direccion':direccion}
  except:
   pedido, created = Pedido.objects.get_or_create(usuario=request.user.id, completado=False)
   context = {'pedido':pedido}
  return render(request, 'polls/cart.html', context)

@login_required
def Midireccion(request):

  
  try:
    midireccion = direccionusuario.objects.get(usuario=request.user.id)
    direccion = direccionform(instance=midireccion)
    context = {'direccion':direccion,'midireccion':midireccion}
  except:
    midireccion = direccionusuario.objects.create(usuario=request.user.id)
    direccion = direccionform(instance=midireccion)
    context = {'direccion':direccion,'midireccion':midireccion}
  return render(request, 'polls/Midireccion.html' ,context) 

@login_required
def Guardardireccion(request):
  direccion = direccionform()
  if request.method == "POST":
    midireccion = direccionusuario.objects.get(usuario=request.user.id)
    direccion = direccionform(request.POST,instance=midireccion)
    ciudad = Ciudad.objects.get(nombre=request.POST["ciudad"])
    midireccion.barrio = request.POST["barrio"]
    midireccion.direccion = request.POST["direccion"]
    midireccion.telefono = request.POST["telefono"]
    midireccion.ciudad = ciudad
    midireccion.save()
    messages.success(request,"Direccion guardada")
    return redirect('Midireccion')


@login_required
def registroproductos(request, pk):
  Productform = ProductoForm()
  
  try:
    Producto = Product.objects.get(id=pk)
    Productform = ProductoForm(instance=Producto)
  except:
    Productform = ProductoForm(request.POST)
  if request.method == "POST":
    if Productform.is_valid(): 
      Productform.save()
      messages.success(request,"Producto guardado")
      return redirect('registroproductos')

  return render(request, 'polls/Registroproductos.html', {'Productform':Productform})

@login_required
def registrarproductos(request):
  Tienda = tienda.objects.get(usuario=request.user.id)
  form = ProductoForm2()
  if request.method == 'POST':
  	form = ProductoForm2(request.POST, request.FILES)
  if form.is_valid():
    form.save()
    return redirect('misproductos')

  context = {'form':form,'Tienda':Tienda}
  return render(request, 'polls/Registroproductos2.html', context)

@login_required
def editarproductos(request, pk):
  producto = Product.objects.get(id=pk)
  form = ProductoForm(instance=producto)
  if request.method == 'POST':
    form = ProductoForm(request.POST,request.FILES, instance=producto)
    if form.is_valid():
     form.save()
     return redirect('misproductos')

  context = {'form':form}
  return render(request, 'polls/Registroproductos.html', context)

@login_required
def eliminarproductos(request, pk):
	producto = Product.objects.get(id=pk)	
	producto.delete()
	return redirect('misproductos')

 
@login_required
def eliminaritem(request):
  if request.method == "POST":
    carritoid = request.POST['carritoid']
    carrito = Carritodecompra.objects.get(id=carritoid)
    carrito.delete()
    messages.success(request,"Item eliminado")
    return redirect('cart')

  return redirect('cart')

@login_required
def confirmardireccion(request):
  customer = request.user.customer
  pedido = Pedido.objects.get(usuario=customer, completado=False)
  direccion = direccionusuario.objects.get(usuario=customer)
  
  context = {'pedido':pedido,'direccion':direccion}
  return render(request, 'polls/pedidosusuario.html', context)


@login_required
def Gestorpedidos(request):
  try:
    
    customer = request.user.customer
  except:
    customer, created = Customer.objects.get_or_create(user=request.user) 

  try:
   pedido = Pedido.objects.filter(completado=True)
   Tienda = tienda.objects.get(usuario=request.user.id)
   Carritodecompras = Carritodecompra.objects.filter(tienda=Tienda)
   confirmado = Carritodecompra.objects.filter(tienda=Tienda, estadoproducto="Confirmado").count
   entregados = Carritodecompra.objects.filter(tienda=Tienda, estadoproducto="Entregado").count
   encamino = Carritodecompra.objects.filter(tienda=Tienda, estadoproducto="En reparto").count
   pendientes = Carritodecompra.objects.filter(tienda=Tienda, estadoproducto="Por confirmar").count
   direccion = direccionusuario.objects.get(usuario=request.user.id)
   estado1 = "Confirmado"
   estado2 = "En reparto"
   estado3 = "Entregado"
   estado4 = "Cancelado"
   estado5 = "Por confirmar" 
   context = {'pedido':pedido,'direccion':direccion,'Carritodecompras':Carritodecompras,'confirmado':confirmado,'entregados':entregados,'encamino':encamino,'pendientes':pendientes,'estado1':estado1,'estado2':estado2,'estado3':estado3,'estado4':estado4,'estado5':estado5}
  except:
   pedido, created = Pedido.objects.get_or_create(usuario=customer, completado=False)
   context = {'pedido':pedido}

  

  return render(request, 'polls/Gestorpedidos.html', context)


@login_required
def Listapedidos(request,pk):
  Tienda = tienda.objects.get(usuario=request.user.id)
  if pk == "Confirmado":
   estado1 = "En reparto"
  if pk == "En reparto":
   estado1 = "Entregado"
  if pk == "Por confirmar":
   estado1 = "Confirmado"
  if pk == "Entregado":
   estado1 = " "
  custom = Customer.objects.all
  pedido = Pedido.objects.filter(completado=True)
  context = {'pk':pk,'custom':custom,'pedido':pedido,'Tienda':Tienda,'estado1':estado1}
  return render(request, 'polls/pedidoslista.html', context)


@login_required
def confirmarpedido(request,pk,es):
  carrito = Carritodecompra.objects.get(id=pk)
  carrito.estadoproducto= estadopedido.objects.get(nombre=es)
  carrito.save()
  messages.success(request,"Pedido confirmado")
  return redirect('Gestorpedidos')



@login_required
def Pedir(request):
  try:
    customer = request.user.customer
  except:
    customer, created = Customer.objects.get_or_create(user=request.user) 
  if request.method == "POST":
    try:
     mipedido = Pedido.objects.get(usuario=request.user.id, completado=False)
     direccion = direccionusuario.objects.get(usuario=request.user.id)
     mipedido.direccion = direccion
     mipedido.completado = True
     mipedido.save()
     messages.success(request,"Pedido Realizado")
     return redirect('mispedidos')
    except:
     messages.success(request,"Faltan datos para continuar")
     return redirect('cart')
