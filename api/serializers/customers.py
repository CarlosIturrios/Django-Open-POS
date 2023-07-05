from django.db.models import Q
from rest_framework import serializers
from mainapp.models import Customer
from mainapp.models import QuantityType
from mainapp.models import Currency
from adminapp.models import Empresa
from adminapp.models import CiudadadPermitida


class CustomerSerializer(serializers.ModelSerializer):
    """
        Serializer rubro para crear, listar y modificar un rubro
    """

    class Meta:
        model = Customer
        fields = (
            'id',
            'name',
            'cellphone',
            'direction',
            'observations',
            'email',
        )
        read_only_fields = (
            'id',
            'name',
            'cellphone',
            'direction',
            'observations',
            'email',
        )


class CiudadadPermitidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CiudadadPermitida
        fields = ['description']


class EmpresaSerializer(serializers.ModelSerializer):
    ciudades_permitidas = CiudadadPermitidaSerializer(many=True, read_only=True, source='ciudades_permitidas.all')

    class Meta:
        model = Empresa
        fields = ['ciudades_permitidas']


class QuantityTypeSerializer(serializers.ModelSerializer):
    """
        
    """
    class Meta:
        model = QuantityType
        fields = (
            'id',
            'description',
            'empresa'
        )
        read_only_fields = (
            'id', 
        )

class CurrencySerializer(serializers.ModelSerializer):
    """
        
    """
    class Meta:
        model = Currency
        fields = (
            'id',
            'description',
            'symbol',
            'empresa'
        )
        read_only_fields = (
            'id', 
        )