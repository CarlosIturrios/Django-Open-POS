from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse
from mainapp import views

app_name = 'mainapp'
urlpatterns = [
    path('spa/', views.Index.as_view(), name='spa_index'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('loutin/', views.LogoutView.as_view(), name='logout'),
    path('categorias/', views.categorias_view, name='categorias'),
    path('productos/<int:pk>', views.productos_view, name='productos'),
    path('eliminar-producto/<int:pk>', views.eliminar_del_carrito, name='eliminar_producto'),
    path('', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='index'),
    path('orden/', views.carrito_view, name='carrito'),
    path('cobrar/', views.cobrar, name='cobrar'),
    path('recibo/<int:pk>', views.GeneratePDF, name='recibo'),
    path('orden-cobrada/<int:pk>', views.orden_cobrada, name='orden_cobrada'),
    path('nueva-orden/', views.crear_nueva_orden, name='crear_nueva_orden'),
    path('detalle-de-la-orden/', views.detalle_de_la_orden, name='detalle_de_la_orden'),
    path('mis-ordenes/', views.mis_ordenes, name='mis_ordenes'),
    path('orden/<int:pk>', views.orden, name='orden'),
]
