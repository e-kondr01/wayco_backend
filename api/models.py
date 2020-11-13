from django.db import models
from django.contrib.auth.models import User


class Cafe(models.Model):
    name = models.CharField(max_length=128, unique=True)
    latitude = models.DecimalField(max_digits=4, decimal_places=2,
                                   null=True, blank=True)
    longitude = models.DecimalField(max_digits=4, decimal_places=2,
                                    null=True, blank=True)
    address = models.CharField(max_length=128)
    average_rating = models.FloatField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    registration_code = models.CharField(max_length=32, unique=True)

    def __str__(self) -> str:
        return f'{self.name}'


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='consumer')
    favourite_cafes = models.ManyToManyField(
        Cafe,
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
    available = models.BooleanField(null=True, blank=True)
    has_options = models.BooleanField()
    on_menu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.name} от {self.created_at}'


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='options')
    name = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'{self.product} {self.name}'


class ProductOptionChoice(models.Model):
    product_option = models.ForeignKey(ProductOption, on_delete=models.CASCADE,
                                       related_name='choices')
    name = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(blank=True, null=True)
    default = models.BooleanField()

    def __str__(self) -> str:
        return f'{self.product_option} {self.name}'


class Order(models.Model):
    order_num = models.CharField(max_length=16,
                                 verbose_name='Номер заказа',
                                 default='undefined')
    total_sum = models.DecimalField(max_digits=8, decimal_places=2,
                                    null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ready_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    consumer = models.ForeignKey(Consumer, on_delete=models.PROTECT,
                                 related_name='orders')
    cafe = models.ForeignKey(Cafe, on_delete=models.PROTECT,
                             related_name='orders')

    STATUS_CHOICES = [
        ('active', 'active'),  # Заказ принят
        ('completed', 'completed'),  # Заказ забрали
        ('ready', 'ready'),  # Заказ готов
        ('unclaimed', 'unclaimed')  # Заказ не забрали
    ]

    status = models.CharField(choices=STATUS_CHOICES, max_length=16)

    def __str__(self) -> str:
        return f'Заказ {self.order_num} от {self.created_at}'

    def calculate_total_sum(self):
        self.total_sum = 0
        for ordered_product in self.ordered_products.all():
            price = 0
            price += ordered_product.product.price
            for chosen_option in ordered_product.chosen_options.all():
                price += chosen_option.price

            self.total_sum += price * ordered_product.quantity


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


class CafeRating(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE,
                                 related_name='ratings')
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE,
                             related_name='ratings')

    VALUE_CHOICES = [
        (1.0, 1.0),
        (1.5, 1.5),
        (2.0, 2.0),
        (2.5, 2.5),
        (3.0, 3.0),
        (3.5, 3.5),
        (4.0, 4.0),
        (4.5, 4.5),
        (5.0, 5.0),
    ]

    value = models.FloatField(choices=VALUE_CHOICES)

    def __str__(self) -> str:
        return f'{self.value} для {self.cafe} от {self.consumer}'


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='employee')
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE,
                             related_name='employees')

    def __str__(self) -> str:
        return f'{self.user}'
