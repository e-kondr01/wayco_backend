from rest_framework import serializers
from common.models import Product, Cafe, ProductOption, ProductOptionChoice


class ProductOptionChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductOptionChoice
        fields = ['id', 'choice_name', 'choice_price']


class ProductOptionSerializer(serializers.ModelSerializer):
    choices = ProductOptionChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOption
        fields = ['id', 'option_name', 'choices']


class ProductSerializer(serializers.ModelSerializer):
    options = ProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image_src', 'options']


class CafeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cafe
        fields = '__all__'
