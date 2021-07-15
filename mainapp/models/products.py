import os
from django.db import models

from mainapp.models import DatosDeControlMixin


def upload_to(instance, filename):
    filename, ext = os.path.splitext(filename)
    return 'products/{}/{}{}'.format(instance.__class__.__name__,
                                     instance.description,
                                     ext
                                     )


class QuantityType(DatosDeControlMixin):
    """
    La tabla contiene la información de las categorías de solicitudes registradas en el sistema.
    """
    description = models.CharField(max_length=100, null=False, blank=False, help_text='Quantity type Description')

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.description)


class Ingredient(DatosDeControlMixin):
    name = models.CharField(max_length=150, null=False, blank=False,
                            help_text='Ingredient name')
    description = models.TextField(null=True, blank=True, help_text='Ingredient description')
    clasification = models.CharField(max_length=15, null=False, blank=False, help_text='Ingrediente clasification')
    quantity = models.IntegerField(null=True, blank=True,
                                   help_text='Ingredient quantity')
    quantity_type = models.ForeignKey('mainapp.QuantityType', on_delete=models.DO_NOTHING,
                                      related_name='relation_QuantityType_Ingredient',
                                      help_text='Fk a la dependencia correspondiente')

    def __str__(self):
        return "{0}".format(self.description)


class Category(DatosDeControlMixin):
    """
    La tabla contiene la información de las categorías de solicitudes registradas en el sistema.
    """
    description = models.CharField(max_length=100, null=False, blank=False,
                                   help_text='Category type Description')
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True,
        help_text='Su imagen se re-dimensionara (200px~100px)',  # translate to english
    )

    def __str__(self):
        return "{0}-{1}".format(self.pk, self.description)


class Product(DatosDeControlMixin):
    product_code = models.CharField(max_length=50, null=False, blank=False,
                                    help_text='Product code')
    name = models.CharField(max_length=150, null=False, blank=False,
                            help_text='Product name')
    description = models.TextField(null=True, blank=True, help_text='Product description')
    category = models.ForeignKey('mainapp.Category', on_delete=models.DO_NOTHING,
                                 related_name='relation_Category_Product',
                                 help_text='Fk to category')
    image = models.ImageField(
        upload_to=upload_to,
        null=True,
        blank=True,
        help_text='Su imagen se re-dimensionara (200px~100px)',  # translate to english
    )
    price = models.DecimalField(max_digits=14, decimal_places=4, help_text='Product price')
    stock = models.IntegerField(null=True, blank=True,
                                help_text='Product stock')
    ingredients = models.ManyToManyField('mainapp.Ingredient', blank=True,
                                         help_text='Fk ingredientes',
                                         related_name='relation_Ingredients_Product')
    barcode = models.CharField(max_length=50, null=False, blank=False,
                               help_text='Product barcode')
    currency = models.ForeignKey('mainapp.Currency', on_delete=models.DO_NOTHING,
                                 related_name='relation_Currency_Product',
                                 help_text='Fk to currency')

    def __str__(self):
        return "{0}-{1}-{2}".format(self.pk, self.name, self.description)
