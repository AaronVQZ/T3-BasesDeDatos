# AppEmpleado/views.py
from django.shortcuts import render, redirect
from django.db import connection

def empleado_home(request):
    # muestra los botones
    return render(request, 'empleado.html')


def consultar_planilla_semanal(request):
    # 1. valida que esté autenticado
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('login')

    # 2. llama al SP
    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC dbo.spConsultarPlanillaSemanal @InUsuarioID = ?", [user_id]
        )
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

    # 3. convierte a lista de dicts
    planillas = [ dict(zip(cols, row)) for row in rows ]

    # 4. renderiza la plantilla con contexto
    return render(request,
                  'planilla_semanal.html',
                  { 'planillas': planillas })


def consultar_planilla_mensual(request):
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('login')

    with connection.cursor() as cursor:
        cursor.execute(
            "EXEC dbo.spConsultarPlanillaMensual @InUsuarioID = ?", [user_id]
        )
        cols = [c[0] for c in cursor.description]
        rows = cursor.fetchall()

    meses = [ dict(zip(cols, row)) for row in rows ]

    return render(request,
                  'planilla_mensual.html',
                  { 'meses': meses })
