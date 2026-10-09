from django.urls import path
from .views import inicio, create, find

urlpatterns = [
    path('home/', inicio, name='inicio'),
    path('create/', create, name='create'),
    path('find/', find, name='find')
]