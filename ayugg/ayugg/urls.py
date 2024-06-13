from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("champdata/", include("main.urls")),
    path('search/', include('user_data.urls')),
    path('ranking/', include('rank_data.urls')),
]