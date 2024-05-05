from django.urls import path

from . import views, apis

urlpatterns = [
    path("champion/", views.write, name="write"),
    path("<int:question_id>/", views.detail, name="detail"),
]
