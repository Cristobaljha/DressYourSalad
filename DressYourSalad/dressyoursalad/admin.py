from django.contrib import admin
from .models import Bowl, Pedido

# Register your models here.

#permite administrar el modelo completo

admin.site.register(Bowl)
admin.site.register(Pedido)