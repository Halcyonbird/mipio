from django.db import models
from datetime import datetime
from psycopg2.extras import DateRange, DateTimeTZRange, NumericRange, Range
from django.contrib.postgres import forms, lookups
from django.contrib.auth.forms import UserCreationForm, User



# Create your models here.
class Ciudad(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, unique=True)
    capital = models.BooleanField(default=False)
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, unique=True )
    minitems = models.IntegerField()
    maxitems = models.IntegerField()
    descuento = models.DecimalField(max_digits=5, decimal_places=2)
    def __str__(self):
        return self.nombre        

class tienda(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.IntegerField(unique=True)
    nombre = models.CharField(max_length=30, unique=True)
    imagen = models.ImageField()
    barrio = models.CharField(max_length=20)
    telefono = models.CharField(max_length=10, unique=True)
    direccion = models.TextField(max_length=40)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True,to_field='nombre')
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True, to_field='nombre')
    Numeroitems = models.IntegerField(null=True,blank=True)
    activa = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

    @property
    def get_nomb(self):
        nomb = self.categoria.nombre
        return nomb

   
    @property
    def get_maxitems(self):
        maxitems = self.categoria.maxitems    
        return maxitems

    @property
    def get_minitems(self):
        minitems = self.categoria.minitems
        return minitems

    @property
    def get_total(self):
        precio = self.Numeroitems * 1000
        descuento = precio * self.categoria.descuento
        total = (precio - descuento)
        return total

class Tiendacustom(models.Model,):
    tienda = models.OneToOneField(tienda, null=True, blank=True, on_delete=models.CASCADE, to_field='nombre')
    fondo = models.ImageField(upload_to="fondos",null=True)

class Categoriaproducto(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.IntegerField()
    nombre = models.CharField(max_length=30, unique=True )
    
    def __str__(self):
        return self.nombre            
    

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to="media", null=True)
    precio = models.IntegerField()
    tiendaid = models.ForeignKey(tienda, on_delete=models.CASCADE, null=True, to_field='nombre')
    categoria = models.ForeignKey(Categoriaproducto, on_delete=models.CASCADE, null=True,to_field='nombre')
    def __str__(self):
        return self.nombre

class estadopedido(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20,unique=True)
    def __str__(self):
        return self.nombre
        
class tipo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, unique=True)
    
    def __str__(self):
        return self.nombre

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)     

class direccionusuario(models.Model):
    usuario = models.IntegerField(unique=True)  
    barrio = models.CharField(max_length=20)
    direccion = models.TextField(max_length=40)
    telefono = models.CharField(max_length=10)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE, null=True, to_field='nombre')   
  

class Pedido(models.Model):
    usuario = models.IntegerField()
    direccion = models.ForeignKey(direccionusuario,null=True,blank=True,on_delete=models.CASCADE)
    completado = models.BooleanField(default=False) 
    fecha = models.DateTimeField(auto_now=True)
  

    def __str__(self):
        return str(self.id)  

    @property
    def get_cart_total(self):
        carritodecompra = self.carritodecompra_set.all()
        total = sum([item.get_total for item in carritodecompra])
        return total 

    @property
    def get_cart_items(self):
        carritodecompra = self.carritodecompra_set.all()
        total = sum([item.cantidad for item in carritodecompra])
        return total 


class Carritodecompra(models.Model):
    id = models.AutoField(primary_key=True)
    productoid = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)       
    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.CASCADE)       
    cantidad = models.IntegerField()
    estadoproducto = models.ForeignKey(estadopedido, null=True, blank=True, on_delete=models.CASCADE, to_field='nombre', default='Por confirmar')
    tienda = models.ForeignKey(tienda, null=True, blank=True, on_delete=models.CASCADE)
    

    @property
    def get_total(self):
        total = self.productoid.precio * self.cantidad
        return total


class Comment(models.Model):
    STATUS = (
        ('Nuevo', 'Nuevo'),
        ('Verdadero', 'Verdadero'),
        ('Falso', 'Falso'),
    )
    tienda=models.ForeignKey(tienda,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='Nuevo')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    
class payudata(models.Model,):
    apikey = models.CharField(max_length=250, blank=True)
    merchantid = models.IntegerField()
    accountId = models.IntegerField()



    
    
    


 


    


    
  