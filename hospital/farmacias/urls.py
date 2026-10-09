from django.urls import path
from .views import inicio, create, find, delete, update

urlpatterns = [
    path('home/', inicio, name='inicio'),
    path('create/', create, name='create'),
    path('find/', find, name='find'),
    path('delete/', delete, name='delete'),
    path('update/', update, name='update')
]