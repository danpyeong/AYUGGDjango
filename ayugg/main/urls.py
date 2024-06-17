from django.urls import path

from . import views

urlpatterns = [
    path('version/', views.version, name='version'),
    path('champion/', views.champion_list, name='champion_list'),
    path('championBasic/', views.champion_basic_info, name='champion_basic_info'),
    path('championStatics/', views.champion_statics, name='champion_statics'),
    path('detail/', views.champion_details, name='champ_details'),
]