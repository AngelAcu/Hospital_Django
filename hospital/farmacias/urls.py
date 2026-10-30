from django.urls import path
from .views import createFarmacia, goIndex, goParams, inicio, create, find, delete, update, createDispensacion, findDispensacion, deleteDispensacion, updateDispensacion

app_name = 'farmacias'

urlpatterns = [
    path('home/', inicio, name='inicio'),
    path('parametros/<int:id>/', goParams, name='params'),
    path('index/<int:decision>/', goIndex, name='index'),
    path('create/', create, name='create'),
    path('find/', find, name='find'),
    path('delete/', delete, name='delete'),
    path('update/', update, name='update'),
    path('createDispensacion/', createDispensacion, name='createDispensacion'),
    path('findDispensacion/', findDispensacion, name='findDispensacion'),
    path('deleteDispensacion/', deleteDispensacion, name='deleteDispensacion'),
    path('updateDispensacion/', updateDispensacion, name='updateDispensacion'),
    path('formulario/', createFarmacia, name='create-farmacia')
]