from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'AppAdministrador'

urlpatterns = [
    path("", views.home, name="home"),
    path("buscar_empleados/", views.buscar_empleados, name="buscar_empleados"),
    path("insertar_empleado/", views.insertar_empleado, name="insertar_empleado"),
    path("editar_empleado/", views.editar_empleado, name="editar_empleado"),
    path("consultar_empleado/", views.consultar_empleado, name="consultar_empleado"),
    
]
