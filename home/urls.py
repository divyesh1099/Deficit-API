from django.urls import path
from home import views
app_name='home'
urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='user_register'),
    path('userfoods/', views.UserFoodListCreate.as_view(), name='userfood-list-create'),
    path('userfoods/<int:pk>/', views.UserFoodRetrieveUpdateDestroy.as_view(), name='userfood-detail'),
]
