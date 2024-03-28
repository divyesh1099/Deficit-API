from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.db.models import Sum, F

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
        return f"{self.user.username}'s {self.food.name} on {self.consumed_datetime}"

    def update_daily_calories(self):
        # This function updates the daily calorie record for the user.
        date = self.consumed_datetime.date()  # Extract the date part from the datetime field.
        daily_calorie_record, created = DailyCalorieRecord.objects.get_or_create(
            user=self.user, 
            date=date,
            defaults={'total_calories': 0}
        )
        # Calculate the total calories for the user for the day.
        total_calories_for_day = UserFood.objects.filter(
            user=self.user, 
            consumed_datetime__date=date
        ).aggregate(
            total=Sum(F('amount') * F('food__calories_per_unit'))
        )['total'] or 0

        daily_calorie_record.total_calories = total_calories_for_day
        daily_calorie_record.save()

    def save(self, *args, **kwargs):
        super(UserFood, self).save(*args, **kwargs)  # Call the "real" save() method.
        self.update_daily_calories()  # Update the daily calories after the UserFood is saved.

    def delete(self, *args, **kwargs):
        super(UserFood, self).delete(*args, **kwargs)  # Call the "real" delete() method.
        self.update_daily_calories()  # Update the daily calories after the UserFood is deleted.

# Ensure that the daily calories are updated even if a UserFood entry is deleted.
@receiver(post_delete, sender=UserFood)
def update_daily_calories_on_delete(sender, instance, **kwargs):
    instance.update_daily_calories()
    
class Exercise(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)  # For example, 'seconds', 'minutes', 'hours', etc.
    calories_burnt_per_unit = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class UserExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_exercises')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercise_entries')
    duration = models.DecimalField(max_digits=6, decimal_places=2)  # Duration for which the exercise was performed
    performed_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s {self.exercise.name} on {self.performed_datetime}"
    
    def update_daily_calories(self):
        date = self.performed_datetime.date()
        daily_calorie_record, created = DailyCalorieRecord.objects.get_or_create(
            user=self.user, 
            date=date,
            defaults={'total_calories': 0}
        )
        total_calories_burned_for_day = UserExercise.objects.filter(
            user=self.user, 
            performed_datetime__date=date
        ).aggregate(
            total=Sum(F('duration') * F('exercise__calories_burnt_per_unit'))
        )['total'] or 0

        daily_calorie_record.total_calories -= total_calories_burned_for_day
        daily_calorie_record.save()

    def save(self, *args, **kwargs):
        super(UserExercise, self).save(*args, **kwargs)
        self.update_daily_calories()

    def delete(self, *args, **kwargs):
        super(UserExercise, self).delete(*args, **kwargs)
        self.update_daily_calories()

@receiver(post_delete, sender=UserExercise)
def update_daily_calories_on_delete(sender, instance, **kwargs):
    instance.update_daily_calories()
    
class DailyCalorieRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_calories')
    date = models.DateField()
    total_calories = models.IntegerField(default=2000)

    class Meta:
        unique_together = [['user', 'date']]
        ordering = ['-date']

    def __str__(self):
        return f'{self.user.username} - {self.date} - {self.total_calories} calories'