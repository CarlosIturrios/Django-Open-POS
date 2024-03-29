# -*- coding: utf-8 -*-
from django_filters import FilterSet

from mainapp.models import Category
from mainapp.models import Product


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = (
            'id',
            'description',
            'empresa',
        )


class ProductFilter(FilterSet):
    class Meta:
        model = Product

        fields = (
            'id',
            'description',
            'category',
            'empresa',
        )
