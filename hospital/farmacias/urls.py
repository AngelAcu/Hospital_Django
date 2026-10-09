from django.urls import path
from .views import inicio, goIndex

urlpatterns = [
    path('home/', inicio, name='inicio'),
    path('index/', goIndex, name='index')
]