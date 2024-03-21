from django.contrib import admin
from .models import *

admin.site.register(Food)
admin.site.register(Exercise)
admin.site.register(UserFood)
admin.site.register(UserExercise)