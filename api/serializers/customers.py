from django.db.models import Q
from rest_framework import serializers
from mainapp.models import Customer


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
