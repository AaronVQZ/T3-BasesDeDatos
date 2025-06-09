# AppEmpleado/views.py
from django.shortcuts import render, redirect
from django.db import connection

def empleado_home(request):
    print("DEBUG: entrando en empleado_home()")
    return render(request, 'empleado.html')


def consultar_planilla_semanal(request):
    print(f"DEBUG: consultar_planilla_semanal() método = {request.method}")
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        print("WARNING: user no autenticado, redirigiendo a login")
        return redirect('login')

    ip_origen = request.META.get('REMOTE_ADDR', '')
    print(f"DEBUG: IP origen = {ip_origen}")

    planillas = []
    try:
        connection.ensure_connection()
        conn = connection.connection

        print(f"DEBUG: SP SpConsultarPlanillaSemanal para user {user_id}")
        sql = """
            EXEC dbo.SpConsultarPlanillaSemanal
              @IdUsuario     = ?,
              @IpOrigen      = ?,
              @OutResultCode = ? OUTPUT
        """
        result = conn.execute(sql, (user_id, ip_origen, 0))
        cols, rows = [c[0] for c in result.description], result.fetchall()
        print(f"INFO: Semanal SP devolvió {len(rows)} filas")
        rows = rows[:15]
        planillas = [dict(zip(cols, r)) for r in rows]
    except Exception as e:
        print("EXCEPTION: fallo SpConsultarPlanillaSemanal")
        print(e)

    return render(request, 'planilla_semanal.html', {'planillas': planillas})


def detalle_deducciones_semanal(request, semana_id):
    print(f"DEBUG: detalle_deducciones_semanal() semana_id={semana_id}")
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('login')

    ip_origen = request.META.get('REMOTE_ADDR', '')
    detalle = []
    try:
        connection.ensure_connection()
        conn = connection.connection

        print(f"DEBUG: SP SpConsultarDetalleDeduccionesSemanales user={user_id} semana={semana_id}")
        sql = """
            EXEC dbo.SpConsultarDetalleDeduccionesSemanales
              @IdUsuario        = ?,
              @IpOrigen         = ?,
              @IdSemanaPlanilla = ?,
              @OutResultCode    = ? OUTPUT
        """
        res = conn.execute(sql, (user_id, ip_origen, semana_id, 0))
        cols, rows = [c[0] for c in res.description], res.fetchall()
        print(f"INFO: Deducciones SP devolvió {len(rows)} filas")
        detalle = [dict(zip(cols, r)) for r in rows]
    except Exception as e:
        print("EXCEPTION: fallo SpConsultarDetalleDeduccionesSemanales")
        print(e)

    return render(request,
                  'detalle_deducciones_semanal.html',
                  {'semana_id': semana_id, 'detalle': detalle})


def detalle_salario_semanal(request, semana_id):
    print(f"DEBUG: detalle_salario_semanal() semana_id={semana_id}")
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('login')

    ip_origen = request.META.get('REMOTE_ADDR', '')
    detalle = []
    try:
        connection.ensure_connection()
        conn = connection.connection

        print(f"DEBUG: SP SpConsultarDetalleSalarioSemanal user={user_id} semana={semana_id}")
        sql = """
            EXEC dbo.SpConsultarDetalleSalarioSemanal
              @IdUsuario        = ?,
              @IpOrigen         = ?,
              @IdSemanaPlanilla = ?,
              @OutResultCode    = ? OUTPUT
        """
        res = conn.execute(sql, (user_id, ip_origen, semana_id, 0))
        cols, rows = [c[0] for c in res.description], res.fetchall()
        print(f"INFO: SalarioDetalle SP devolvió {len(rows)} filas")
        detalle = [dict(zip(cols, r)) for r in rows]
    except Exception as e:
        print("EXCEPTION: fallo SpConsultarDetalleSalarioSemanal")
        print(e)

    return render(request,
                  'detalle_salario_semanal.html',
                  {'semana_id': semana_id, 'detalle': detalle})


def consultar_planilla_mensual(request):
    print(f"DEBUG: consultar_planilla_mensual() método = {request.method}")
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('login')

    ip_origen = request.META.get('REMOTE_ADDR', '')
    meses = []
    try:
        connection.ensure_connection()
        conn = connection.connection

        print(f"DEBUG: SP SpConsultarPlanillaMensual user={user_id}")
        sql = """
            EXEC dbo.SpConsultarPlanillaMensual
              @IdUsuario     = ?,
              @IpOrigen      = ?,
              @OutResultCode = ? OUTPUT
        """
        res = conn.execute(sql, (user_id, ip_origen, 0))
        cols, rows = [c[0] for c in res.description], res.fetchall()
        print(f"INFO: Mensual SP devolvió {len(rows)} filas")
        rows = rows[:12]
        meses = [dict(zip(cols, r)) for r in rows]
    except Exception as e:
        print("EXCEPTION: fallo SpConsultarPlanillaMensual")
        print(e)

    return render(request, 'planilla_mensual.html', {'meses': meses})

def detalle_deducciones_mensual(request, mes_id):
    print(f"DEBUG: detalle_deducciones_mensual() mes_id={mes_id}")
    user_id = request.session.get('_auth_user_id')
    if not user_id:
        return redirect('login')

    ip_origen = request.META.get('REMOTE_ADDR', '')
    detalle = []
    try:
        connection.ensure_connection()
        conn = connection.connection

        print(f"DEBUG: SP SpConsultarDetalleDeduccionMensuales user={user_id} mes={mes_id}")
        sql = """
            EXEC dbo.SpConsultarDetalleDeduccionesMensuales
              @IdUsuario       = ?,
              @IpOrigen        = ?,
              @IdMesPlanilla   = ?,
              @OutResultCode   = ? OUTPUT
        """
        res = conn.execute(sql, (user_id, ip_origen, mes_id, 0))
        cols, rows = [c[0] for c in res.description], res.fetchall()
        print(f"INFO: Detalle mensual SP devolvió {len(rows)} filas")
        detalle = [dict(zip(cols, r)) for r in rows]
    except Exception as e:
        print("EXCEPTION: fallo SpConsultarDetallededuccionMensuales")
        print(e)

    return render(request,
                  'detalle_deducciones_mensual.html',
                  {'mes_id': mes_id, 'detalle': detalle})
