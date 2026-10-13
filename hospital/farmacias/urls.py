from django.urls import path
from .views import inicio, create, find, delete, update, createDispensacion, findDispensacion, deleteDispensacion, updateDispensacion

urlpatterns = [
    path('home/', inicio, name='inicio'),
    path('create/', create, name='create'),
    path('find/', find, name='find'),
    path('delete/', delete, name='delete'),
    path('update/', update, name='update'),
    path('createDispensacion/', createDispensacion, name='createDispensacion'),
    path('findDispensacion/', findDispensacion, name='findDispensacion'),
    path('deleteDispensacion/', deleteDispensacion, name='deleteDispensacion'),
    path('updateDispensacion/', updateDispensacion, name='updateDispensacion')
]