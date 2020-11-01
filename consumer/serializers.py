from django.contrib.auth.models import User
from rest_framework import serializers

from common.models import Order, Cafe, Consumer
from common.serializers import CafeSerializer


class ConsumerSerializer(serializers.ModelSerializer):
    favourite_cafes = CafeSerializer(many=True)

    class Meta:
        model = Consumer
        fields = ['favourite_cafes']


class ConsumerInfoSerializer(serializers.ModelSerializer):
    consumer = ConsumerSerializer()

    class Meta:
        model = User
        fields = ['id', 'consumer']
