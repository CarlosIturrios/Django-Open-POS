from django_filters import FilterSet

from mainapp.models import Customer
from mainapp.models import QuantityType
from mainapp.models import Currency

class CustomerFilter(FilterSet):
    class Meta:
        model = Customer
        fields = (
            'id',
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