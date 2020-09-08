from django.contrib import admin
from .models import Product, tienda, Ciudad, estadopedido, Categoria, Categoriaproducto, Carritodecompra, Pedido, Customer, Comment, payudata, Tiendacustom, direccionusuario
# Register your models here.

admin.site.register(Product)


admin.site.register(tienda)
admin.site.register(estadopedido)
admin.site.register(Ciudad)
admin.site.register(Categoria)
admin.site.register(Categoriaproducto)
admin.site.register(Carritodecompra)
admin.site.register(Pedido)
admin.site.register(Customer)
admin.site.register(Comment)
admin.site.register(payudata)
admin.site.register(Tiendacustom)
admin.site.register(direccionusuario)
