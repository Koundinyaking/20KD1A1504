
from django.urls import path
from . import views

urlpatterns = [
    path('numbers/', views.get_numbers), 
]