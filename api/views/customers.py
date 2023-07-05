from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response


from mainapp.models import Customer
from mainapp.models import QuantityType
from mainapp.models import Currency
from adminapp.models import Empresa

from api.filters import CustomerFilter
from api.filters import QuantityTypeFilter
from api.filters import CurrencyFilter

from api.serializers import CustomerSerializer
from api.serializers import EmpresaSerializer
from api.serializers import QuantityTypeSerializer
from api.serializers import CurrencySerializer



class CustomerView(ReadOnlyModelViewSet):
    """

    """
    
    queryset = Customer.objects.filter(eliminado=False)
    serializer_class = CustomerSerializer
    filterset_class = CustomerFilter

class EmpresaView(APIView):
    def get(self, request, cadena):
        empresa = get_object_or_404(Empresa, nombre_para_pagos=cadena)
        serializer = EmpresaSerializer(empresa)
        return Response(serializer.data)


class QuantityTypeView(viewsets.ModelViewSet):
    """

    """
    
    queryset = QuantityType.objects.filter(eliminado=False)
    serializer_class = QuantityTypeSerializer
    filterset_class = QuantityTypeFilter


class CurrencyView(viewsets.ModelViewSet):
    """

    """
    
    queryset = Currency.objects.filter(eliminado=False)
    serializer_class = CurrencySerializer
    filterset_class = CurrencyFilter
    
