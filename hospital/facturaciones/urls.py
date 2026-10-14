from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio),
    path('create/', views.create),
    path('find/', views.find),
    path('update/', views.update),
    path('delete/', views.delete),
]