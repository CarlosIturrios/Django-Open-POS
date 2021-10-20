from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

from mainapp.models import Customer

from api.filters import CustomerFilter

from api.serializers import CustomerSerializer


class CustomerView(ReadOnlyModelViewSet):
    """

    """
    permission_classes = (IsAuthenticated,)
    queryset = Customer.objects.filter(eliminado=False)
    serializer_class = CustomerSerializer
    filterset_class = CustomerFilter
