from django.contrib.auth.models import User
from rest_framework import serializers
from common.models import (
    Product, Cafe, ProductOption, ProductOptionChoice, Order, OrderedProduct,
    )


class ProductOptionChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOptionChoice
        fields = ['id', 'name', 'price', 'is_available', 'is_default']


class ProductOptionSerializer(serializers.ModelSerializer):
    choices = ProductOptionChoiceSerializer(many=True)

    class Meta:
        model = ProductOption
        fields = ['id', 'name', 'choices']


class BackwardProductOptionSerializer(serializers.ModelSerializer):
    '''This serializer is needed to view order history. '''

    class Meta:
        model = ProductOption
        fields = ['id', 'name']


class BackwardProductOptionChoiceSerializer(serializers.ModelSerializer):
    '''This serializer is needed to view order history. '''
    product_option = BackwardProductOptionSerializer()

    class Meta:
        model = ProductOptionChoice
        fields = ['id', 'option', 'name', 'price']


class ProductSerializer(serializers.ModelSerializer):
    '''This serializer is needed to view product's detials. '''
    options = ProductOptionSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_src',
                  'options', 'is_available']


class ProductSerializerForHistory(serializers.ModelSerializer):
    '''This serializer is needed to view order history. '''

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_src']


class ProductSerializerForMenu(serializers.ModelSerializer):
    '''This serializer is needed to view cafe's products. '''

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_src',
                  'is_available', 'has_options']


class CafeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cafe
        fields = '__all__'


class ViewOrderedProductSerializer(serializers.ModelSerializer):
    chosen_options = BackwardProductOptionChoiceSerializer(
        many=True, required=False)
    product = ProductSerializerForHistory()

    class Meta:
        model = OrderedProduct
        fields = ['quantity', 'product', 'chosen_options']


class CreateOrderedProductSerializer(serializers.ModelSerializer):
    chosen_options = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=ProductOptionChoice.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderedProduct
        fields = ['quantity', 'product', 'chosen_options']


class CreateOrderSerializer(serializers.ModelSerializer):
    ordered_products = CreateOrderedProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_num', 'total_sum', 'status', 'ordered_products']

    def create(self, validated_data):
        ordered_products_data = validated_data.pop('ordered_products')
        order = Order.objects.create(**validated_data)

        for ordered_product_data in ordered_products_data:
            chosen_options_data = ordered_product_data.pop('chosen_options')
            ordered_product = OrderedProduct.objects.create(
                order=order, **ordered_product_data)
            for chosen_option in chosen_options_data:
                ordered_product.chosen_options.add(chosen_option)

        order.calculate_total_sum()
        order.order_num = 'W' + str(order.pk % 100)
        order.save()

        return order


class ViewOrderSerializer(serializers.ModelSerializer):
    ordered_products = ViewOrderedProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'order_num', 'total_sum', 'status', 'ordered_products']
