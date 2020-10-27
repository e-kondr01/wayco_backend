from django.db import models
from accounts.models import *


class Cafe(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    longitude = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    address = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.name}'


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.name}'


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='options')
    option_name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.product} {self.option_name}'


class ProductOptionChoice(models.Model):
    product_option = models.ForeignKey(ProductOption, on_delete=models.PROTECT,
                                       related_name='choices')
    choice_name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.product_option} {self.choice_name}'


class Order(models.Model):
    order_num = models.CharField(max_length=16,
                                 verbose_name='Номер заказа')

    def __str__(self) -> str:
        return f'Заказ {self.order_num}'


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='ordered_products')
    quantity = models.PositiveSmallIntegerField()
    chosen_options = models.ForeignKey(ProductOptionChoice,
                                       on_delete=models.PROTECT,
                                       related_name='ordered_products')
    order = models.ForeignKey(Order, on_delete=models.PROTECT,
                              related_name='ordered_products')

    def __str__(self) -> str:
        return f'Заказанный {self.product}'
