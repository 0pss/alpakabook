from django.urls import path
from . import views

urlpatterns = [
    path('', views.userpage),
    path("<int:user_id>/", views.userpage, name="userpage"),
]