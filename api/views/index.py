# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from rest_framework import viewsets
from adminapp.models import HorarioAcceso
from api.serializers import HorarioAccesoSerializer
from api.filters import HorarioAccesoFilter


class HorariosDeAccesoView(viewsets.ModelViewSet):
    """

    """
    
    queryset = HorarioAcceso.objects.filter(eliminado=False)
    serializer_class = HorarioAccesoSerializer
    filterset_class = HorarioAccesoFilter