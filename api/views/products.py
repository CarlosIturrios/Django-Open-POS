from django.contrib.auth import get_user_model
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from mainapp.models import Category
from mainapp.models import Product

from api.filters import CategoryFilter
from api.filters import ProductFilter

from api.serializers import CategorySerializer
from api.serializers import ProductSerializer


class CategoryView(ReadOnlyModelViewSet):
    """
        Vista de Rubro para crear, modificar y listar rubros
    """
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.filter(eliminado=True)
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter


class ProductView(ReadOnlyModelViewSet):
    """
        Vista de Rubro para crear, modificar y listar rubros
    """
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
