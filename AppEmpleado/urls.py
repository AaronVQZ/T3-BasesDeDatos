# AppEmpleado/urls.py
from django.urls import path
from . import views

app_name = 'AppEmpleado'

urlpatterns = [
    path('', views.empleado_home, name='home'),
    path('planilla/semanal/', views.consultar_planilla_semanal, name='planilla_semanal'),
    path('planilla/semanal/deducciones/<int:semana_id>/', views.detalle_deducciones_semanal, name='detalle_deducciones_semanal'),
    path('planilla/semanal/detalle/<int:semana_id>/', views.detalle_salario_semanal,     name='detalle_salario_semanal'),
    path('planilla/mensual/',  views.consultar_planilla_mensual,  name='planilla_mensual'),
    path('planilla/mensual/deducciones/<int:mes_id>/', views.detalle_deducciones_mensual, name='detalle_deducciones_mensual'),
]
