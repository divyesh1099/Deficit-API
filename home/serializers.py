from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserFood

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