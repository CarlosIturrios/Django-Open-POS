from django.contrib import admin
# Register your models here.
from .models import *

admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
