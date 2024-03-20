from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import status, views
from rest_framework.response import Response
from home.serializers import UserSerializer
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

def index(requests):
    return render(requests, 'home/index.html')

class UserCreate(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserFoodListCreate(generics.ListCreateAPIView):
    queryset = UserFood.objects.all()
    serializer_class = UserFoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user sees only their own food entries
        return UserFood.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)

# Retrieve, Update, Delete UserFood
class UserFoodRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserFood.objects.all()
    serializer_class = UserFoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user can only update their own food entries
        return UserFood.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        user_food = self.get_object()
        # Check if 'amount' is in the request and if it is set to 0
        if 'amount' in request.data and request.data['amount'] == 0:
            user_food.delete()  # Delete the user food entry
            return Response({'detail': 'User food entry deleted because amount was set to 0.'}, status=status.HTTP_204_NO_CONTENT)
        return super().update(request, *args, **kwargs)
    
class FoodList(APIView):
    def get(self, request, format=None):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)