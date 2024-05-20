from django.urls import path

from . import views

urlpatterns = [
    path('champion/', views.champion_list, name='champion_list'),
]