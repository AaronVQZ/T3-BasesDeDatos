from Excepciones import excepciones as excepciones
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime, date
from django.db import connection
import json

# Create your views here.
def home(request):

    try:
        id_usuario = request.session.get("_auth_user_id")
        ip_usuario = request.session.get("_auth_user_ip")
        termino_por_buscar = ''
        #empleados = obtener_empleados(termino_por_buscar,id_usuario,ip_usuario)
        #empleados = obtener_empleados(search_query)
        empleados = obtener_empleados(termino_por_buscar, id_usuario=id_usuario, ip_usuario=ip_usuario)
        return render(request, 'administrador.html', {'empleados': empleados})
    except Exception as e:
        return render(request, 'administrador.html',{ 
                      'error': 'Error al obtener los empleados: ' + str(e)})
    

def obtener_empleados(search_term='',id_usuario=None,ip_usuario=None):
    
    try:    
        connection.ensure_connection()
        conn = connection.connection
        codigo_error = 0

        empleados = conn.execute("""
                EXEC Sp_BuscarEmpleado 
                @InSearchTerm = ?
               ,@InIdUsuario = ?
               ,@InIpUsuario = ?
               ,@OutCodigoError = ? OUTPUT
                                 
                """,(search_term, int(id_usuario), str(ip_usuario), codigo_error)).fetchall()
                
        if codigo_error != 0:
            raise excepciones.Error_obtener_empleados()    
        # Se convierten los resultados a una lista de diccionarios
        empleados_list = [{'id': row[0], 'nombre': row[1],'puesto': row[2], } for row in empleados]
        return empleados_list if empleados else []
    except Exception as e:
        print(f"Error al obtener empleados: {e}")
        return []  
    

def buscar_empleados(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            id_usuario = request.session.get("_auth_user_id")
            ip_usuario = request.session.get("_auth_user_ip")
            termino_por_buscar = request.GET.get("term", '')
            empleados = obtener_empleados(termino_por_buscar,id_usuario,ip_usuario)
            
            return JsonResponse({"success": True, "empleados": empleados}, safe=False)

        except Exception as e:
            return JsonResponse({"success": True, "error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


def insertar_empleado(request):
    if request.method == "POST":
        
        # Obtener los datos del formulario
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        tipo_usuario = request.POST.get("tipo_usuario", "").strip()
        nombre = request.POST.get("nombre", "").strip()
        id_tipo_documento = request.POST.get("id_tipo_documento", "").strip()
        valor_documento = request.POST.get("valor_documento", "").strip()
        fecha_nacimiento = request.POST.get("fecha_nacimiento", "").strip()
        id_puesto = request.POST.get("id_puesto", "").strip()
        id_departamento = request.POST.get("id_departamento", "").strip()

        #formato de fecha
        fecha = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        fecha_nacimiento = fecha.date()
              
        id_usuario = request.session.get("_auth_user_id")
        ip_usuario = request.session.get("_auth_user_ip")
        codigo_error = 0

        try:
            #Asegurar la conexion
            connection.ensure_connection()
            conn = connection.connection

            conn.execute(
                "EXEC dbo.Sp_InsertarEmpleado ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? OUTPUT",
                [id_usuario, ip_usuario, username, password, int(tipo_usuario), 
                 nombre, int(id_tipo_documento), valor_documento, 
                 fecha_nacimiento, int(id_puesto), int(id_departamento), codigo_error]
            )

            # Si no hay excepción, devolvemos JSON de éxito
            return JsonResponse({"success": True, "mensaje": "Empleado insertado correctamente"})

        except Exception as e:
            # Capturar cualquier error que lance el THROW del SP
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    # Si no es POST AJAX
    return JsonResponse({"success": False, "error": "Método no permitido."}, status=400)


def editar_empleado(request):
    if request.method == "POST":
        
        # Obtener los datos del formulario
        id_empleado = request.POST.get('id_empleado', '').strip()
        nombre = request.POST.get("nombre", "").strip()
        id_tipo_documento = request.POST.get("id_tipo_documento", "").strip()
        valor_documento = request.POST.get("valor_documento", "").strip()
        fecha_nacimiento = request.POST.get("fecha_nacimiento", "").strip()
        id_puesto = request.POST.get("id_puesto", "").strip()
        id_departamento = request.POST.get("id_departamento", "").strip()

        #formato de fecha
        fecha = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
        fecha_nacimiento = fecha.date()
              
        id_usuario = request.session.get("_auth_user_id")
        ip_usuario = request.session.get("_auth_user_ip")
        codigo_error = 0
        try:
            #Asegurar la conexion
            connection.ensure_connection()
            conn = connection.connection
            

            conn.execute(
                "EXEC dbo.Sp_EditarEmpleado ?, ?, ?, ?, ?, ?, ?, ?, ?, ? OUTPUT",
                [id_usuario, ip_usuario, int(id_empleado) ,nombre, int(id_tipo_documento), valor_documento, 
                 fecha_nacimiento, int(id_puesto), int(id_departamento), codigo_error]
            )

            # Si no hay excepción, devolvemos JSON de éxito
            return JsonResponse({"success": True, "mensaje": "Datos editados correctamente"})

        except Exception as e:
            # Capturar cualquier error que lance el THROW del SP
            print(f"Error al editar empleado: {e}, ")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    # Si no es POST AJAX
    return JsonResponse({"success": False, "error": "Método no permitido."}, status=400)


def consultar_empleado(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        id_empleado = request.GET.get('id_empleado', '').strip()
        codigo_error = 0
        try:
            connection.ensure_connection()
            conn = connection.connection
            row = conn.execute(
                "EXEC dbo.Sp_ConsultarEmpleado ?, ? OUTPUT",
                [int(id_empleado), codigo_error]
            ).fetchone()

            if not row:
                return JsonResponse({"success": False, "error": "Empleado no encontrado"}, status=404)

            empleado = {
                "nombre": row[0],
                "tipoDocumento":row[1],
                "valorDocumento":row[2],
                "fechaNacimiento":row[3].strftime('%Y-%m-%d') if row[3] else None,
                "departamento": row[4],
                "puesto": row[5],
            }
            return JsonResponse({"success": True, "empleado": empleado})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Invalid request"}, status=400)


def eliminar_empleado(request):
    if request.method == "POST":
        id_empleado = request.POST.get('id_empleado', '').strip()
        id_usuario = request.session.get("_auth_user_id")
        ip_usuario = request.session.get("_auth_user_ip")
        codigo_error = 0

        try:
            connection.ensure_connection()
            conn = connection.connection
            conn.execute(
                "EXEC dbo.Sp_EliminarEmpleado ?, ?, ?, ? OUTPUT",
                [int(id_usuario), str(ip_usuario), int(id_empleado), codigo_error]
            )
            
            return JsonResponse({"success": True, "mensaje": "Empleado eliminado correctamente"})
        except Exception as e:
            print(f"Error al eliminar empleado: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Método no permitido."}, status=400)


def impersonar_empleado(request):
    if request.method == "GET":
        id_empleado = request.GET.get('id_empleado', '').strip()
        id_usuario_impersonado = 0

        try: 
            connection.ensure_connection()
            conn = connection.connection

            
            row = conn.execute(
                "EXEC dbo.Sp_GetIdUsuario ?, ? OUTPUT",
                [int(id_empleado), 0]
            ).fetchone()

            if not row:
                return JsonResponse({"success": False, "error": "Empleado no encontrado"}, status=404)
        
            id_usuario_impersonado = row[0]
            request.session['_id_empleado_impersonado'] = id_usuario_impersonado
            return JsonResponse({"success": True, "redirect": "/empleado"})

        except Exception as e:
            print(f"Error al obtener ID de usuario: {e}")
            return JsonResponse({"success": False, "error": str(e)}, status=500)
