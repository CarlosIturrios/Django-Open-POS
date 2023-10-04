# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta

from adminapp.models import Empresa
# Create your views here.
def website(request):
    return render(request, 'website/index_website.html')

def fuera_de_horario(request, pk):
    empresa = Empresa.objects.get(pk=pk)
    hora_actual = timezone.now()
    hora_actual_hermosillo = hora_actual - timedelta(hours=7)
    hora_actual = hora_actual_hermosillo.time()
    hora_inicio = empresa.horario_de_acceso.hora_inicio
    hora_fin = empresa.horario_de_acceso.hora_fin
    nombre_comercial = empresa.nombre_comercial
    nombre_para_pagos = empresa.nombre_para_pagos
    
    context = {
        'hora_actual': hora_actual,
        'hora_inicio': hora_inicio,
        'hora_fin': hora_fin,
        'nombre_comercial': nombre_comercial,
        'nombre_para_pagos': nombre_para_pagos,
    }

    return render(request, 'website/fuera_de_horario.html', context)
