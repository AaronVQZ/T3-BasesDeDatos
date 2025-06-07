# AppEmpleado/urls.py
from django.urls import path
from . import views

app_name = 'AppEmpleado'

urlpatterns = [
    # página principal con los botones
    path('', views.empleado_home, name='home'),

    # vistas que renderizan los grids
    path('planilla/semanal/', views.consultar_planilla_semanal, name='planilla_semanal'),
    path('planilla/mensual/',  views.consultar_planilla_mensual,  name='planilla_mensual'),
]
