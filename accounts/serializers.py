from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password


class ConsumerUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirmation = serializers.CharField(
            min_length=8, write_only=True)

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):

        user = User.objects.create_user(validated_data['username'],
                                        password=validated_data['password'])
        group = Group.objects.get(name='consumers')
        user.groups.add(group)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirmation')


class CafeBaristaUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        password=validated_data['password'])
        group = Group.objects.get(name='cafe_baristas')
        user.groups.add(group)

        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
