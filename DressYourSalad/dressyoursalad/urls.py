from django.urls import URLPattern, path
from .views import index,pago, form_crear, form_modificar,form_eliminar,form_ver, registro, form_pedido, reservar_carrito, seguir_comprando, ver_carrito,form_ver_pedidos, form_eliminar_carrito, form_entregado, form_pagado, form_nopagado, dashboard, form_noentregado, form_ver_pagados,form_reportevtas, form_buscar_pedidos, form_update_pedido, form_bowls
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', index, name="index"),
   
    path('pago', pago, name="pago"),
    path('form_ver', form_ver, name="form_ver"),
    path('form_crear', form_crear, name="form_crear"),
    path('form_modificar/<id>', form_modificar, name="form_modificar"),
    path('form_eliminar/<id>', form_eliminar, name="form_eliminar"),
    path('form_pedido', form_pedido, name="form_pedido"),
    path('reservar_carrito/<id>', reservar_carrito, name="reservar_carrito"),
    path('seguir_comprando/<id>', seguir_comprando, name="seguir_comprando"),
    path('ver_carrito/<id>', ver_carrito, name="ver_carrito"),
    
    path('form_eliminar_carrito/<id>/<id2>', form_eliminar_carrito, name="form_eliminar_carrito"),

    path('registro', registro, name="registro"),
    path('accounts/login/', LoginView.as_view(template_name='loginadmin/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='loginadmin/logout.html'), name='logout'),
    path('form_ver_pedidos/<boleta>/<id_carrito>', form_ver_pedidos, name="form_ver_pedidos"),
    path('form_ver_pagados', form_ver_pagados, name="form_ver_pagados"),
    path('form_reportevtas/<dia>', form_reportevtas, name="form_reportevtas"),
    path('form_buscar_pedidos/<id_c>', form_buscar_pedidos, name="form_buscar_pedidos"),
    path('form_update_pedido/<id_c>/<boleta>/<pagado>/<entregado>', form_update_pedido, name="form_update_pedido"),

    path('form_entregado/<id>', form_entregado, name="form_entregado"),
    path('form_noentregado/<id>', form_noentregado, name="form_noentregado"),
    path('form_pagado/<id>', form_pagado, name="form_pagado"),
    path('form_nopagado/<id>', form_nopagado, name="form_nopagado"),
    path('dashboard', dashboard, name="dashboard"),
    
    path('form_bowls', form_bowls, name="form_bowls"),

]