from django_filters import FilterSet

from mainapp.models import Category
from mainapp.models import Product


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = (
            'id',
            'description',
        )


class ProductFilter(FilterSet):
    class Meta:
        model = Product

        fields = (
            'id',
            'description',
            'category',
        )
