from django.urls import path, include
from django.conf.urls import url
from .views import registrousuario, hacerpedido, inicio, mispedidos, registrotienda, confirmacionregistro, confirmacionregistrotienda, Menuproductos, Vistaproducto, agregaralcarrito, cart, pagomenbresiatienda, mitienda, guadarfondo, misproductos, eliminaritem, Midireccion, Pedir, confirmardireccion, registroproductos, registrarproductos, editarproductos, eliminarproductos, Gestorpedidos, Listapedidos, confirmarpedido, Guardardireccion
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [

     # ex: /polls/inicio
     path('registrousuario/',registrousuario, name='registrousuario'),
     path('registrotienda/',registrotienda, name='registrotienda'),
     path('confirmacionregistro/',confirmacionregistro, name='confirmacionregistro'),
     path('confirmacionregistrotienda/',confirmacionregistrotienda, name='confirmacionregistrotienda'),
     path('',inicio, name='inicio'),
     path('inicio/',inicio, name='inicio'),
     path('mitienda/',mitienda, name='mitienda'),
     path('guadarfondo/',guadarfondo, name='guadarfondo'),
     path('mispedidos/',mispedidos, name='mispedidos'),
     path('misproductos/',misproductos, name='misproductos'),
     path('hacerpedido/',hacerpedido, name='hacerpedido'),
     path('Menuproductos/',Menuproductos, name='Menuproductos'),
     path('Vistaproducto/', Vistaproducto, name='Vistaproducto'),
     path('agregaralcarrito/', agregaralcarrito, name='agregaralcarrito'),
     path('cart/', cart, name='cart'), 
     path('Pedir/', Pedir, name='Pedir'),
     path('eliminaritem/', eliminaritem, name='eliminaritem'),
     path('pagomenbresiatienda/', pagomenbresiatienda, name='pagomenbresiatienda'),
     path('Midireccion/', Midireccion, name='Midireccion'),
     path('confirmardireccion/', confirmardireccion, name='confirmardireccion'),
     path('registroproductos/<str:pk>/', registroproductos, name='registroproductos'),
     path('registrarproductos/', registrarproductos, name='registrarproductos'),
     path('editarproductos/<str:pk>/', editarproductos, name='editarproductos'),
     path('eliminarproductos/<str:pk>/', eliminarproductos, name='eliminarproductos'),
     path('Gestorpedidos',Gestorpedidos, name='Gestorpedidos'),
     path('Listapedidos/<str:pk>/', Listapedidos, name='Listapedidos'),
     path('confirmarpedido/<str:pk>/<str:es>/', confirmarpedido, name='confirmarpedido'),
     path('Guardardireccion',Guardardireccion, name='Guardardireccion'),
   
 



    

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

