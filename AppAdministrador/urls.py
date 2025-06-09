from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'AppAdministrador'

urlpatterns = [
    path("", views.home, name="home"),
    path("buscar_empleados/", views.buscar_empleados, name="buscar_empleados"),
    path("insertar_empleado/", views.insertar_empleado, name="insertar_empleado"),
    
]
