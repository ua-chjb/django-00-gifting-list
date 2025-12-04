from django.views.generic import RedirectView
from django.urls import path
from . import views

app_name = "main_list"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),
    path("calculator/", views.calculator, name="calculator"),
    path("add/", views.add_item, name="add_item_general"),
    path("<str:person_name>/", views.items, name="items"),
    path("<str:person_name>/add", views.add_item, name="add_item"),
    path("delete/<int:item_id>/", views.delete_item, name="delete_item")
]