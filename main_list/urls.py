from django.views.generic import RedirectView
from django.urls import path
from . import views

app_name = "main_list"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("", views.years, name="years"),
    path("<int:year>/", views.index, name="index"),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),
    path("<int:year>/calculator/", views.calculator, name="calculator"),
    path("<int:year>/add/", views.add_item, name="add_item_general"),
    path("<int:year>/<str:person_name>/", views.items, name="items"),
    # path("<int:year>/<str:person_name>/add", views.add_item, name="add_item"),
    path("delete/<int:item_id>/", views.delete_item, name="delete_item")
]