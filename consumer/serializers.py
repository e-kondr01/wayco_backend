from django.contrib.auth.models import User
from rest_framework import serializers

from common.models import CafeRating, Order, Cafe, Consumer
from common.serializers import CafeSerializer


class ConsumerSerializer(serializers.ModelSerializer):
    favourite_cafes = CafeSerializer(many=True)

    class Meta:
        model = Consumer
        fields = ['favourite_cafes']


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
        fields = ['consumer', 'cafe', 'value']
