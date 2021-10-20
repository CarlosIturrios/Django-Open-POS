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
urlpatterns = [
    path('', include(router.urls)),
]
