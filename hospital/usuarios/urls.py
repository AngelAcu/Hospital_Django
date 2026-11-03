from django.urls import path
from .views import inicio, create, find, delete, update, iniciar_sesion, cerrar_sesion

urlpatterns = [
    path('home/', inicio, name='inicio_usuario'),
    path('login/', iniciar_sesion, name='login_usuario'),
    path('logout/', cerrar_sesion, name='logout_usuario'),
    path('create/', create, name='create_usuario'),
    path('find/', find, name='find_usuario'),
    path('delete/<int:id>/', delete, name='delete_usuario'),
    path('update/<int:id>/', update, name='update_usuario'),
]
