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
from django.utils.timezone import localtime
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

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
        user_food = serializer.save(user=self.request.user)  # Save to get the instance
        self.update_daily_calories(user_food, created=True)

    def update_daily_calories(self, user_food, created):
        consumed_date = localtime(user_food.consumed_datetime).date()
        daily_calorie_record, _ = DailyCalorieRecord.objects.get_or_create(
            user=user_food.user, 
            date=consumed_date,
            defaults={'total_calories': 0}
        )
        if created:
            daily_calorie_record.total_calories += user_food.amount * user_food.food.calories_per_unit
            daily_calorie_record.save()

# Retrieve, Update, Delete UserFood
class UserFoodRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserFood.objects.all()
    serializer_class = UserFoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user can only update their own food entries
        return UserFood.objects.filter(user=self.request.user).exclude(amount=0)
    
    def update(self, request, *args, **kwargs):
        user_food = self.get_object()
        # Ensure 'amount' is interpreted as an integer
        if 'amount' in request.data:
            try:
                amount = int(request.data['amount'])
                if amount == 0:
                    user_food.delete()
                    return Response({'detail': 'User food entry deleted because amount was set to 0.'}, status=status.HTTP_204_NO_CONTENT)
            except ValueError:  # In case the amount is not a valid integer
                return Response({'error': 'Amount must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)
    
class FoodList(APIView):
    def get(self, request, format=None):
        foods = Food.objects.all()
        serializer = FoodSerializer(foods, many=True)
        return Response(serializer.data)
    

class ExerciseList(APIView):
    def get(self, request, format=None):
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        return Response(serializer.data)
    
# List and create user exercises
class UserExerciseListCreate(generics.ListCreateAPIView):
    queryset = UserExercise.objects.all()
    serializer_class = UserExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user sees only their own exercise entries
        return UserExercise.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)

# Retrieve, Update, Delete UserExercise
class UserExerciseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserExercise.objects.all()
    serializer_class = UserExerciseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure a user can only manipulate their own exercise entries
        return UserExercise.objects.filter(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        user_exercise = self.get_object()
        # Check if 'duration' is in the request and if it is set to 0
        if 'duration' in request.data and request.data['duration'] == 0:
            user_exercise.delete()  # Delete the user exercise entry
            return Response({'detail': 'User exercise entry deleted because duration was set to 0.'}, status=status.HTTP_204_NO_CONTENT)
        return super().update(request, *args, **kwargs)
    
class DailyCalorieRecordListCreate(generics.ListCreateAPIView):
    queryset = DailyCalorieRecord.objects.all()
    serializer_class = DailyCalorieRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class DailyCalorieRecordRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = DailyCalorieRecord.objects.all()
    serializer_class = DailyCalorieRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class CalorieRecordByDateView(APIView):
    """
    Fetch the calorie record for the current user by date.
    """
    permission_classes = [IsAuthenticated]

    @method_decorator(csrf_exempt)
    def get(self, request, date):
        user = request.user
        try:
            calorie_record = DailyCalorieRecord.objects.get(user=user, date=date)
            return JsonResponse({
                'date': date,
                'total_calories': calorie_record.total_calories
            })
        except DailyCalorieRecord.DoesNotExist:
            raise Http404("No calorie record found for this date.")