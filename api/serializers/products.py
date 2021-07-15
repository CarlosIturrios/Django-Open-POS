from django.db.models import Q
from rest_framework import serializers
from mainapp.models import Category
from mainapp.models import Product


class CategorySerializer(serializers.ModelSerializer):
    """
        Serializer rubro para crear, listar y modificar un rubro
    """

    class Meta:
        model = Category
        fields = (
            'id',
            'description',
            'image',
        )
        read_only_fields = (
            'id',
            'description',
            'image',
        )


class ProductSerializer(serializers.ModelSerializer):
    """
        Serializer rubro para crear, listar y modificar un rubro
    """

    class Meta:
        model = Product

        category = CategorySerializer(many=False, read_only=True)
        fields = (
            'id',
            'product_code',
            'description',
            'name',
            'category',
            'image',
            'price',
            'stock',
            'barcode',
            'currency',
            'ingredients',
        )
        read_only_fields = (
            'id',
            'product_code',
            'description',
            'name',
            'category',
            'image',
            'price',
            'stock',
            'barcode',
            'currency',
            'ingredients',
        )
