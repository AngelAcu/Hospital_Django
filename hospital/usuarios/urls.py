from django.urls import path
from .views import inicio, create, find, delete, update

urlpatterns = [
    path('home/', inicio, name='inicio_usuario'),
    path('create/', create, name='create_usuario'),
    path('find/', find, name='find_usuario'),
    path('delete/', delete, name='delete_usuario'),
    path('update/', update, name='update_usuario'),
]