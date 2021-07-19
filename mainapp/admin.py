from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import *


class CategoryResources(resources.ModelResource):
    class Meta:
        model = Category


class CategoryImportExport(ImportExportModelAdmin):
    resource_class = CategoryResources


class OrderResources(resources.ModelResource):
    class Meta:
        model = Order


class OrderImportExport(ImportExportModelAdmin):
    resource_class = OrderResources


admin.site.register(Level)
admin.site.register(Status)
admin.site.register(OrderDetail)
admin.site.register(Order, OrderImportExport)
admin.site.register(QuantityType)
admin.site.register(Category, CategoryImportExport)
admin.site.register(Ingredient)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Currency)
admin.site.register(OrderType)
admin.site.register(Place)

