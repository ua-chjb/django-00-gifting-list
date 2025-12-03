from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("main_list.urls")),
    path('admin/', admin.site.urls),
]
