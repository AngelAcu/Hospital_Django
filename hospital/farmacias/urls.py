from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_medicamento, name='inicio_medicamento'),
    path('medicamentos/create/', views.create_medicamento, name='create_medicamento'),
    path('medicamentos/find/', views.find_medicamento, name='find_medicamento'),
    path('medicamentos/update/<str:id>/', views.update_medicamento, name='update_medicamento'),
    path('medicamentos/delete/<str:id>/', views.delete_medicamento, name='delete_medicamento'),
]