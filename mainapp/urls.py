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
]
