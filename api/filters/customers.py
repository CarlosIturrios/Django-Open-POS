from django_filters import FilterSet

from mainapp.models import Customer


class CustomerFilter(FilterSet):
    class Meta:
        model = Customer
        fields = (
            'id',
            'cellphone',
            'email',
        )
