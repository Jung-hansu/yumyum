from django.contrib import admin
from django.urls import path
from reviewManagement import views

urlpatterns = [
    path('stars/', views.starAverage),
    path('stars/input', views.inputData),
    path('category/', views.getCategory),
    path('mood/', views.getMood),
]
