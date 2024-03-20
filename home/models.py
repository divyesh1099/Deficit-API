from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)  # For example, 'grams', 'pieces', etc.
    calories_per_unit = models.DecimalField(max_digits=6, decimal_places=2)  # Or IntegerField, depending on your needs

    def __str__(self):
        return self.name
    
class UserFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_foods')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='food_entries')
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    consumed_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.food.name} on {self.consumed_date}"