from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio_cita'),
    path('create/', views.create, name='create_cita'),
    path('find/', views.find, name='find_cita'),
    path('update/<str:id>/', views.update, name='update_cita'),
    path('delete/<str:id>/', views.delete, name='delete_cita'),
]