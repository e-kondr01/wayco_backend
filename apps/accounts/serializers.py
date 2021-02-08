from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer)

from .models import Consumer, Cafe, Employee


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
        consumer = Consumer(user=user)
        consumer.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirmation')


class EmployeeUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
            max_length=32,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)
    password_confirmation = serializers.CharField(
            min_length=8, write_only=True)
    registration_code = serializers.CharField(max_length=32)

    def validate_registration_code(self, value):
        if not Cafe.objects.filter(registration_code=value).first():
            raise serializers.ValidationError("Incorrect registration code.")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        cafe = Cafe.objects.filter(
            registration_code=validated_data['registration_code']).first()
        user = User.objects.create_user(validated_data['username'],
                                        password=validated_data['password'])
        employees = Group.objects.get(name='employees')
        user.groups.add(employees)
        consumers = Group.objects.get(name='consumers')
        user.groups.add(consumers)
        employee = Employee(user=user, cafe=cafe)
        employee.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'registration_code', 'username',
                  'password', 'password_confirmation')
