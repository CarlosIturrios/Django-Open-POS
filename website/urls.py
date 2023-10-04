# -*- coding: utf-8 -*-
from django.urls import path
from website import views

app_name = 'website'
urlpatterns = [
    path('', views.website, name='website'),
    path('sin-horario/<int:pk>', views.fuera_de_horario, name='fuera_de_horario'),
]
