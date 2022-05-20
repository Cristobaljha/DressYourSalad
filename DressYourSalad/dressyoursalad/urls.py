from django.urls import URLPattern, path
from .views import index, carrito,pago, form_crear, form_modificar,form_eliminar,form_ver, registro
from django.contrib.auth.views import LoginView, LogoutView


# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('', index, name="index"),
    path('carrito', carrito, name="carrito"),
    path('pago', pago, name="pago"),
    path('form_ver', form_ver, name="form_ver"),
    path('form_crear', form_crear, name="form_crear"),
    path('form_modificar/<id>', form_modificar, name="form_modificar"),
    path('form_eliminar/<id>', form_eliminar, name="form_eliminar"),
    path('registro', registro, name="registro"),
    # path('login', login, name="login"),
    path('accounts/login/', LoginView.as_view(template_name='logincli/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logincli/logout.html'), name='logout'),
    # path('logout/',login_required(logout),name = 'logout'),

]