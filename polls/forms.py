from django import forms
from django.forms import ModelForm
from .models import Product, tienda, Carritodecompra, Comment, Tiendacustom, Ciudad, direccionusuario
from django.contrib.auth.forms import User, UserCreationForm

   


class ProductoForm2(ModelForm):
   
   class Meta:
      model = Product
      fields = ['nombre','imagen','precio','categoria','tiendaid']    
      widgets = {
       'nombre': forms.TextInput(attrs={'class':'input100','placeholder':'Nombre'}),
       'imagen': forms.FileInput(attrs={'class':'input100','placeholder':'Imagen'}),
       'precio': forms.NumberInput(attrs={'class':'input100','placeholder':'Precio'}),
       'categoria' : forms.Select(attrs={'class':'input100','placeholder':'categoria'}),
      }

class ProductoForm(ModelForm):
   
   class Meta:
      model = Product
      fields = ['nombre','imagen','precio','categoria']    
      widgets = {
       'nombre': forms.TextInput(attrs={'class':'input100','placeholder':'Nombre'}),
       'imagen': forms.FileInput(attrs={'class':'input100','placeholder':'Imagen'}),
       'precio': forms.NumberInput(attrs={'class':'input100','placeholder':'Precio'}),
       'categoria' : forms.Select(attrs={'class':'input100','placeholder':'categoria'}),
      }



class ciudadForm(ModelForm):
   
   class Meta:
      model = Ciudad
      fields = ['nombre']    
      widgets = {
       'nombre': forms.Select(attrs={'class':'input100','placeholder':'Ciudad'}),
      }


class direccionform(ModelForm):
   
   class Meta:
      model = direccionusuario
      fields = ['usuario','barrio','telefono','direccion','ciudad']    
      widgets = {
       'barrio': forms.TextInput(attrs={'class':'input100','placeholder':'Barrio'}),
       'telefono': forms.NumberInput(attrs={'class':'input100','placeholder':'Telefono','min':'1000000000','max':'9999999999'}),
       'direccion': forms.TextInput(attrs={'class':'input100','placeholder':'Direccion'}),
       'ciudad': forms.Select(attrs={'class':'input100','placeholder':'Ciudad'}),
      }



class TiendaForm(ModelForm):
   
   class Meta:
      model = tienda
      fields = ['usuario','nombre','imagen','barrio','telefono','direccion','categoria','ciudad']    
      widgets = {
       'categoria': forms.Select(attrs={'class':'input100','placeholder':'Categoria'}),
       'ciudad': forms.Select(attrs={'class':'input100','placeholder':'Ciudad'}),
      }

class TiendaForm2(ModelForm):
   
   class Meta:
      model = tienda
      fields = ['Numeroitems']    

class TiendacustomForm(ModelForm):
   
   class Meta:
      model = Tiendacustom
      fields = ['fondo']    
      widgets = {
       'fondo': forms.FileInput(attrs={'class':'input100'}),
       
      }

class CarritoForm(ModelForm):
   
   class Meta:
      model = Carritodecompra
      fields = ['productoid','cantidad','pedido']   


class Registrousuario(UserCreationForm):
   
   class Meta:
      model = User
      fields = ['username','password1','password2','first_name','last_name','email']
      

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


