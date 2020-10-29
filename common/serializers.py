from rest_framework import serializers
from common.models import Product, Cafe


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class CafeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cafe
        fields = '__all__'