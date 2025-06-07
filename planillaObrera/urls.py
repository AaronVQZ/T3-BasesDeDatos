from django.contrib import admin
from django.urls import path, include
from AppLogin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login, name="login"),
    path('login/', include('AppLogin.urls')),
    path('administrador/', include('AppAdministrador.urls', namespace='AppAdministrador')),
    path('empleado/', include('AppEmpleado.urls', namespace='AppEmpleado')),
]
