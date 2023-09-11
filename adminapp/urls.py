# -*- coding: utf-8 -*-
from django.urls import path
from django.views.generic import RedirectView
from django.urls import reverse
from adminapp import views

app_name = 'administracion'
urlpatterns = [
    path('registrar-empresa/', views.registrar_empresa, name='registrar_empresa'),
    path('empresas/', views.listar_empresas, name='listar_empresas'),
    path('empresas/actualizar/<int:empresa_id>/', views.actualizar_empresa, name='actualizar_empresa'),
    path('acceder/<int:pk>', views.acceder, name='acceder'),
    path('registro/', views.registro, name='registro'),
]
