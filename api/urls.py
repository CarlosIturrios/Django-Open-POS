from django.urls import include
from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse

from rest_framework import routers

from api import views

app_name = 'api'

router = routers.DefaultRouter()

router.register('categories', views.CategoryView)
router.register('products', views.ProductView)
router.register('customers', views.CustomerView)
router.register('tipos-de-ingredientes', views.QuantityTypeView)
router.register('monedas', views.CurrencyView)
urlpatterns = [
    path('', include(router.urls)),
    path('empresa/<str:cadena>/', views.EmpresaView.as_view(), name='empresa'),
    path('webhooks/mercado-pago/<str:cadena>/', views.MercadoPagoWebHook.as_view(), name='MercadoPagoWebHook'),

]
