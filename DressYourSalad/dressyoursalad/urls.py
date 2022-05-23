from django.urls import URLPattern, path
from .views import index,pago, form_crear, form_modificar,form_eliminar,form_ver, registro, form_pedido, form_carrito, form_ver_pedidos, form_eliminar_carrito, form_entregado, form_pagado, form_nopagado, form_noentregado, form_boleta, form_ver_pagados,form_boleta2, form_bowls,  ListaPedidosListView, ListPedidosPdf
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name="index"),
   
    path('pago', pago, name="pago"),
    path('form_ver', form_ver, name="form_ver"),
    path('form_crear', form_crear, name="form_crear"),
    path('form_modificar/<id>', form_modificar, name="form_modificar"),
    path('form_eliminar/<id>', form_eliminar, name="form_eliminar"),
    path('form_pedido', form_pedido, name="form_pedido"),
    path('form_carrito', form_carrito, name="form_carrito"),
    
    path('form_eliminar_carrito/<id>', form_eliminar_carrito, name="form_eliminar_carrito"),

    path('registro', registro, name="registro"),
    path('accounts/login/', LoginView.as_view(template_name='loginadmin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='loginadmin/logout.html'), name='logout'),
    path('form_ver_pedidos', form_ver_pedidos, name="form_ver_pedidos"),

    path('form_ver_pagados', form_ver_pagados, name="form_ver_pagados"),

    path('form_boleta/<id>', form_boleta, name="form_boleta"),
    path('form_boleta2/<id>', form_boleta2, name="form_boleta2"),

    path('form_entregado/<id>', form_entregado, name="form_entregado"),
    path('form_noentregado/<id>', form_noentregado, name="form_noentregado"),
    path('form_pagado/<id>', form_pagado, name="form_pagado"),
    path('form_nopagado/<id>', form_nopagado, name="form_nopagado"),
    
    path('form_bowls', form_bowls, name="form_bowls"),

    path('lista/', ListaPedidosListView.as_view(),name='lista'),
    path('reporte', ListPedidosPdf.as_view(), name='pedidos_all'),
]