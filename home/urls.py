from django.urls import path
from home import views
app_name='home'
urlpatterns = [
    path('', views.index, name='index'),
    path('foods/', views.FoodList.as_view(), name='food-list'),
    path('exercises/', views.ExerciseList.as_view(), name='exercise-list'),
    path('register/', views.UserCreate.as_view(), name='user_register'),
    path('userfoods/', views.UserFoodListCreate.as_view(), name='userfood-list-create'),
    path('userfoods/<int:pk>/', views.UserFoodRetrieveUpdateDestroy.as_view(), name='userfood-detail'),
    path('userexercises/', views.UserExerciseListCreate.as_view(), name='userexercise-list-create'),
    path('userexercises/<int:pk>/', views.UserExerciseRetrieveUpdateDestroy.as_view(), name='userexercise-detail'),
    path('calories/', views.DailyCalorieRecordListCreate.as_view(), name='calorie-record-list-create'),
    path('calories/<int:pk>/', views.DailyCalorieRecordRetrieveUpdateDestroy.as_view(), name='calorie-record-detail'),
    path('calories/<str:date>/', views.CalorieRecordByDateView.as_view(), name='calorie_record_by_date'),
]
