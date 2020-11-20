from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class ProductOptionChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOptionChoice
        fields = ['id', 'name', 'price', 'available', 'default']


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
        fields = ['id', 'product_option', 'name', 'price']


class ProductSerializerForHistory(serializers.ModelSerializer):
    '''This serializer is needed to view order history. '''

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_src']


class ProductSerializer(serializers.ModelSerializer):
    '''This serializer is needed to create a new product and
       view product's details '''
    options = ProductOptionSerializer(many=True, required=False)
    available = serializers.BooleanField(required=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_src', 'available',
                  'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options')
        has_options = True if options_data else False
        product = Product.objects.create(has_options=has_options,
                                         **validated_data)

        for option_data in options_data:
            choices_data = option_data.pop('choices')
            option = ProductOption.objects.create(
                product=product, **option_data)
            for choice_data in choices_data:
                choice = ProductOptionChoice.objects.create(
                    product_option=option, **choice_data)

        return product


class ProductSerializerForMenu(serializers.ModelSerializer):
    '''This serializer is needed to view cafe's products.
    (doesn't include product options)'''

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_src',
                  'available', 'has_options']


class ViewOrderedProductSerializer(serializers.ModelSerializer):
    chosen_options = BackwardProductOptionChoiceSerializer(
        many=True, required=False)
    product = ProductSerializerForHistory()

    class Meta:
        model = OrderedProduct
        fields = ['id', 'quantity', 'product', 'chosen_options']


class CreateOrderedProductSerializer(serializers.ModelSerializer):
    chosen_options = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=ProductOptionChoice.objects.all())
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = OrderedProduct
        fields = ['id', 'quantity', 'product', 'chosen_options']


class CreateOrderSerializer(serializers.ModelSerializer):
    ordered_products = CreateOrderedProductSerializer(many=True)
    cafe = serializers.PrimaryKeyRelatedField(queryset=Cafe.objects.all())
    status = serializers.CharField(max_length=16, required=False)
    order_num = serializers.CharField(max_length=16, required=False)
    total_sum = serializers.DecimalField(max_digits=8, decimal_places=2,
                                         required=False)

    class Meta:
        model = Order
        fields = ['id', 'order_num', 'total_sum', 'status',
                  'cafe', 'ordered_products']

    def create(self, validated_data):
        ordered_products_data = validated_data.pop('ordered_products')
        order = Order.objects.create(status='active', **validated_data)

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


class ViewActiveOrderSerializerForConsumer(serializers.ModelSerializer):
    ordered_products = ViewOrderedProductSerializer(many=True)
    cafe = serializers.PrimaryKeyRelatedField(queryset=Cafe.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'cafe', 'order_num', 'created_at', 'total_sum',
                  'status', 'ordered_products']


class ViewActiveOrderSerializerForEmployee(serializers.ModelSerializer):
    ordered_products = ViewOrderedProductSerializer(many=True)
    consumer = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'consumer', 'order_num', 'created_at', 'total_sum',
                  'status', 'ordered_products']


class ViewCompletedOrderSerializerForConsumer(serializers.ModelSerializer):
    ordered_products = ViewOrderedProductSerializer(many=True)
    cafe = serializers.PrimaryKeyRelatedField(queryset=Cafe.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'cafe', 'order_num', 'created_at', 'completed_at',
                  'total_sum', 'status', 'ordered_products', ]


class ViewCompletedOrderSerializerForEmployee(serializers.ModelSerializer):
    ordered_products = ViewOrderedProductSerializer(many=True)
    consumer = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = ['id', 'consumer', 'order_num', 'created_at',
                  'ready_at', 'completed_at', 'total_sum', 'status',
                  'ordered_products']


class CafePhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CafePhoto
        fields = ['id', 'image_src']


class CafeSerializer(serializers.ModelSerializer):
    photos = CafePhotoSerializer(many=True)

    class Meta:
        model = Cafe
        fields = ['id', 'name', 'photos', 'average_rating', 'latitude',
                  'longitude', 'address', 'description']
        read_only_fields = ['average_rating']

    def update(self, instance, validated_data):
        photos_data = validated_data.pop('photos')

        instance.name = validated_data.get('name', instance.name)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get(
            'longitude', instance.longitude)
        instance.address = validated_data.get('address', instance.address)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        return instance


class ConsumerSerializer(serializers.ModelSerializer):
    favourite_cafes = CafeSerializer(many=True)

    class Meta:
        model = Consumer
        fields = ['id', 'favourite_cafes']


class ConsumerUserInfoSerializer(serializers.ModelSerializer):
    consumer = ConsumerSerializer()

    class Meta:
        model = User
        fields = ['id', 'consumer']


class CafeRatingSerializer(serializers.ModelSerializer):
    consumer = serializers.PrimaryKeyRelatedField(
        queryset=Consumer.objects.all())
    cafe = serializers.PrimaryKeyRelatedField(queryset=Cafe.objects.all())

    class Meta:
        model = CafeRating
        fields = ['id', 'consumer', 'cafe', 'value']
