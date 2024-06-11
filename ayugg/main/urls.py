from django.urls import path

from . import views

urlpatterns = [
    path('version/', views.version, name='version'),
    path('champion/', views.champion_list, name='champion_list'),
    path('championStatics/', views.champion_statics, name='champion_statics'),
]