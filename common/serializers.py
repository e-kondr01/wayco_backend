from rest_framework import serializers
from common.models import (Product, Cafe,
    ProductOption, ProductOptionChoice, Order, OrderedProduct)


class ProductOptionChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOptionChoice
        fields = ['id', 'choice_name', 'choice_price']


class ProductOptionSerializer(serializers.ModelSerializer):
    choices = ProductOptionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOption
        fields = ['id', 'option_name', 'choices']


class BackwardProductOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOption
        fields = ['id', 'option_name',]


class BackwardProductOptionChoiceSerializer(serializers.ModelSerializer):
    product_option = BackwardProductOptionSerializer()

    class Meta:
        model = ProductOptionChoice
        fields = ['id', 'product_option', 'choice_name', 'choice_price']


class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_src', 'options']


class ProductNoOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_src']


class CafeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cafe
        fields = '__all__'


class OrderedProductSerializer(serializers.ModelSerializer):
    chosen_options = BackwardProductOptionChoiceSerializer(many=True, read_only=True)
    product = ProductNoOptionsSerializer()

    class Meta:
        model = OrderedProduct
        fields = ['quantity', 'product', 'chosen_options']


class OrderSerializer(serializers.ModelSerializer):
    ordered_products = OrderedProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_num', 'total_sum', 'status', 'ordered_products']
