from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

class GetLogoutView(auth_views.LogoutView):
    http_method_names = ["get", "post", "options"]

urlpatterns = [
    path('admin/', admin.site.urls),

    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", GetLogoutView.as_view(), name="logout"),
    path("", include("main_list.urls"))
]
