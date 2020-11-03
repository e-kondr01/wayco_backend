from django.db import models
from django.contrib.auth.models import User


class Cafe(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.DecimalField(max_digits=4, decimal_places=2,
                                   null=True, blank=True)
    longitude = models.DecimalField(max_digits=4, decimal_places=2,
                                    null=True, blank=True)
    address = models.CharField(max_length=128)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='consumer')
    favourite_cafes = models.ManyToManyField(Cafe,
                                             related_name='consumers_favourite',
                                             blank=True)

    def __str__(self) -> str:
        return f'{self.user}'


class CafePhoto(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE,
                             related_name='photos')
    image_src = models.URLField()

    def __str__(self) -> str:
        return f'{self.cafe} photo'


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image_src = models.URLField(null=True, blank=True)
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE,
                             related_name='products')

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
    choice_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self) -> str:
        return f'{self.product_option} {self.choice_name}'


class Order(models.Model):
    order_num = models.CharField(max_length=16,
                                 verbose_name='Номер заказа',
                                 default=0)
    total_sum = models.DecimalField(max_digits=8, decimal_places=2, blank=True,
                                    default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    done_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32)
    consumer = models.ForeignKey(Consumer, on_delete=models.PROTECT,
                                 related_name='orders')

    def __str__(self) -> str:
        return f'Заказ {self.order_num} от {self.created_at}'

    def calculate_total_sum(self):
        for ordered_product in self.ordered_products.all():
            self.total_sum += ordered_product.product.price
            for chosen_option in ordered_product.chosen_options.all():
                self.total_sum += chosen_option.choice_price


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT,
                                related_name='ordered_products')
    quantity = models.PositiveSmallIntegerField(default=1)
    chosen_options = models.ManyToManyField(ProductOptionChoice,
                                            related_name='ordered_products',
                                            blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='ordered_products')

    def __str__(self) -> str:
        return f'Заказанный {self.product}'
