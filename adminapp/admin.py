# -*- coding: utf-8 -*-
from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(CiudadadPermitida, CiudadadPermitidaAdmin)
admin.site.register(PaymentWithMercadoPago, PaymentWithMercadoPagoAdmin)
admin.site.register(HorarioAcceso, HorarioAccesoAdmin)
