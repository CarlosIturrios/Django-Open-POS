from django_filters import FilterSet, CharFilter

from mainapp.models import Customer
from mainapp.models import QuantityType
from mainapp.models import Currency
from adminapp.models import HorarioAcceso

class CustomerFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = (
            'id',
            'name',
            'cellphone',
            'email',
            'empresa',
        )


class QuantityTypeFilter(FilterSet):
    class Meta:
        model = QuantityType
        fields = (
            'id',
            'description',
            'empresa',
        )

class CurrencyFilter(FilterSet):
    class Meta:
        model = Currency
        fields = (
            'id',
            'description',
            'empresa',
        )        

class HorarioAccesoFilter(FilterSet):
    class Meta:
        model = HorarioAcceso
        fields = (
            'id',
            'hora_inicio',
            'hora_fin',
        )        