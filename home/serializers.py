from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserFoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFood
        fields = ['id', 'user', 'food', 'amount', 'consumed_datetime']
        read_only_fields = ('user',)

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['id', 'name', 'unit', 'calories_per_unit']

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'unit', 'calories_burnt_per_unit']

class UserExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExercise
        fields = ['id', 'user', 'exercise', 'duration', 'performed_datetime']
        read_only_fields = ('user',)