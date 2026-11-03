from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio_historia'),
    path('create/', views.create, name='create_historia'),
    path('find/', views.find, name='find_historia'),
    path('update/<int:id>/', views.update, name='update_historia'),
    path('delete/<int:id>/', views.delete, name='delete_historia'),
]
