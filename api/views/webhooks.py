from django.shortcuts import get_object_or_404
import mercadopago
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
# from rest_framework import viewsets
from rest_framework.response import Response


# from mainapp.models import Customer
# from mainapp.models import QuantityType
from adminapp.models import Empresa
from adminapp.models import PaymentWithMercadoPago

# from api.filters import CustomerFilter
# from api.filters import QuantityTypeFilter
# from api.filters import CurrencyFilter

# from api.serializers import CustomerSerializer
# from api.serializers import EmpresaSerializer
# from api.serializers import QuantityTypeSerializer
# from api.serializers import CurrencySerializer

class MercadoPagoWebHook(APIView):
    def post(self, request, *args, **kwargs):
        cadena = kwargs.get('cadena')
        empresa = get_object_or_404(Empresa, nombre_para_pagos=cadena)
        sdk = mercadopago.SDK(empresa.sdk_private)
        pago = sdk.payment().get(request.data['data']['id'])
        try:       
            pago = PaymentWithMercadoPago.objects.get(external_reference=pago['response']['external_reference'], pagado=False)
            pago.action = request.data['action']
            pago.api_version = request.data['api_version']
            pago.data = request.data['data']
            pago.data_id = request.data['data']['id']
            pago.date_created = request.data['date_created']
            pago.live_mode = request.data['live_mode']
            pago.payment_type = request.data['type']
        except:    
            pago = PaymentWithMercadoPago()
            pago.action = request.data['action']
            pago.api_version = request.data['api_version']
            pago.data = request.data['data']
            pago.data_id = request.data['data']['id']
            pago.date_created = request.data['date_created']
            pago.live_mode = request.data['live_mode']
            pago.payment_type = request.data['type']
            pago.external_reference=pago['response']['external_reference']
            pago.payment_id = request.data['id']    
            #TODO MANDAR UN CORREO AL ADMINISTRADOR DE LA EMPRESA PARA VER QUE SHOW CON ESTE PAGO QUE NO LO TENEMOS EN EL SISTEMA 
        pago.save()
        return Response(status=200)