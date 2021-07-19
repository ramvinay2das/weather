from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'weather-home'), 
    path('day/', views.day_forecast, name = 'weather-multi-forecast'), 
    path('modify-city/', views.modify_city, name = 'modify-city'), 
]