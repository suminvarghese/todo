# from dataclasses import field
from asyncore import read
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Todos

class Todoserializer(serializers.ModelSerializer):
    status=serializers.CharField(read_only=True)
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Todos
        fields=["task_name","user","status"]
    def create(self, validated_data):
        usr=self.context.get("user")
        return Todos.objects.create(**validated_data,user=usr)

class Registrationserializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","email","username","password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
