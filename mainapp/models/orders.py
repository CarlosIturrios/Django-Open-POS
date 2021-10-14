from django.db import models
from django.contrib.auth.models import User

from mainapp.models import DatosDeControlMixin


class Status(DatosDeControlMixin):
    """
    La tabla contiene la información de las categorías de solicitudes registradas en el sistema.
    """
    description = models.CharField(max_length=100, null=False, blank=False, help_text='Status type Description')

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.description)


class OrderType(DatosDeControlMixin):
    """
    La tabla contiene la información de las categorías de solicitudes registradas en el sistema.
    """
    description = models.CharField(max_length=100, null=False, blank=False, help_text='Order Type Description')

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.description)


class Place(DatosDeControlMixin):
    """
    La tabla contiene la información de las categorías de solicitudes registradas en el sistema.
    """
    description = models.CharField(max_length=100, null=False, blank=False, help_text='Place Description')
    direction = models.TextField(null=False, blank=False, help_text='Place Direction')
    empresa = models.ForeignKey('adminapp.Empresa', null=False, blank=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.description)


class Level(DatosDeControlMixin):
    """
    La tabla contiene la información de las categorías de solicitudes registradas en el sistema.
    """
    description = models.CharField(max_length=100, null=False, blank=False, help_text='Place Description')
    priority = models.IntegerField(null=True, blank=True,
                                   help_text='Level Priority', unique=True)

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.description)


class Order(DatosDeControlMixin):
    comments = models.TextField(null=False, blank=False, help_text='Place Direction')
    approved = models.DateTimeField(null=False, blank=False, auto_now=True)
    done = models.DateTimeField(null=True, blank=True, auto_now=False)
    cashier = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                related_name='relacion_Cashier_a_Order',
                                help_text='Fk a usuario para conocer el usuario que cobro la orden')
    cook = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                             related_name='relacion_Cook_a_Order',
                             help_text='Fk a usuario para conocer el usuario que cocinara la orden')
    waiter = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='relacion_Waiter_a_Order', default=None,
                               help_text='Fk a usuario para conocer el usuario que tiene la orden como mesero')
    dealer = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='relacion_Dealer_a_Order', default=None,
                               help_text='Fk a usuario para conocer el usuario que entrego la orden')
    customer = models.ForeignKey('mainapp.Customer', on_delete=models.DO_NOTHING, null=True, blank=True,
                                 related_name='relacion_Customer_a_Order',
                                 help_text='Fk a usuario para conocer pagara la orden de existir')
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True,
                                related_name='relacion_Manager_a_Order',
                                help_text='Fk a usuario para conocer el usuario que creo el registro')
    status = models.ForeignKey('mainapp.Status', on_delete=models.DO_NOTHING, null=True, blank=True,
                               related_name='relacion_Status_a_Order',
                               help_text='Fk a usuario para conocer el usuario que creo el registro')
    level = models.ForeignKey('mainapp.Level', on_delete=models.DO_NOTHING, null=True, blank=True,
                              related_name='relacion_Level_a_Order',
                              help_text='Fk a usuario para conocer el usuario que creo el registro')
    place = models.ForeignKey('mainapp.Place', on_delete=models.DO_NOTHING, null=True, blank=True,
                              related_name='relacion_Place_a_Order',
                              help_text='Fk a usuario para conocer el usuario que creo el registro')
    order_type = models.ForeignKey('mainapp.OrderType', on_delete=models.DO_NOTHING, null=True, blank=True,
                                   related_name='relacion_OrderType_a_Order', default=None,
                                   help_text='Fk to Order Type')

    amount = models.DecimalField(max_digits=14, decimal_places=4, help_text='Product price', default=0)
    change = models.DecimalField(max_digits=14, decimal_places=4, help_text='Product price', default=0)
    cash_paid = models.DecimalField(max_digits=14, decimal_places=4, help_text='Product price', default=0)
    subtotal = models.DecimalField(max_digits=14, decimal_places=4, help_text='Product price', default=0)
    taxes = models.DecimalField(max_digits=14, decimal_places=4, help_text='Product price', default=0)
    empresa = models.ForeignKey('adminapp.Empresa', null=False, blank=False, on_delete=models.DO_NOTHING)
    pagado = models.BooleanField(default=False,
                                 help_text='Parametro que nos dira si la orden ya se ha pagado')
    cocinado = models.BooleanField(default=False,
                                   help_text='Parametro que nos dira si la orden ya se ha cocinado')
    entregado = models.BooleanField(default=False,
                                    help_text='Parametro que nos dira si la orden ya se ha entregado al cliente')

    def __str__(self):
        return "comments: {0}, total: {1}, status: {2}".format(self.comments, self.amount, self.status.description)


class OrderDetail(DatosDeControlMixin):
    quantity = models.IntegerField(null=True, blank=True,
                                   help_text='OrderDetail quantity')
    order = models.ForeignKey('mainapp.Order', on_delete=models.DO_NOTHING, null=True, blank=True,
                              related_name='relacion_Order_a_OrderDetail',
                              help_text='Fk a usuario para conocer el usuario que creo el registro')
    product = models.ForeignKey('mainapp.Product', on_delete=models.DO_NOTHING, null=True, blank=True,
                                related_name='relacion_Product_a_OrderDetail',
                                help_text='Fk a usuario para conocer el usuario que creo el registro')
    empresa = models.ForeignKey('adminapp.Empresa', null=False, blank=False, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Product: {0}, quantity: {1}, order #{2}".format(self.product.name, self.quantity, self.order.pk)
