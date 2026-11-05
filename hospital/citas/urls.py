from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('create/', views.create, name='create'),
    path('find/', views.find, name='find'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
]