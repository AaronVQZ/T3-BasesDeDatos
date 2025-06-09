from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json
from datetime import datetime, date
from Excepciones import excepciones as excepciones


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
    



#-------------------------------------------------------------
# Función para obtener empleados desde la base de datos
def obtener_empleados(search_term='',id_usuario=None,ip_usuario=None):
    
    try:    
        connection.ensure_connection()
        conn = connection.connection
        codigo_error = 0

        empleados = conn.execute("""
                DECLARE @OutCodigoError INT;
                EXEC Sp_BuscarEmpleado 
                @InSearchTerm = ?
               ,@InIdUsuario = ?
               ,@InIpUsuario = ?
               ,@OutCodigoError = ?
                                 
                """,(search_term, int(id_usuario), str(ip_usuario), codigo_error)).fetchall()
                
        if codigo_error != 0:
            raise excepciones.Error_obtener_empleados()    
        # Se convierten los resultados a una lista de diccionarios
        empleados_list = [{'id': row[0], 'nombre': row[1],'puesto': row[2], } for row in empleados]
        return empleados_list if empleados else []
    except Exception as e:
        print(f"Error al obtener empleados: {e}")
        return []  
    
#-------------------------------------------------------------
# Función para manejar la búsqueda de empleados desde AJAX
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


#-------------------------------------------------------------
# Función para insertar un nuevo empleado
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

        print("Datos recibidos para insertar empleado:")
        print(f"Username: {username}, Tipo Usuario: {tipo_usuario}, Nombre Empleado: {nombre}, ID Tipo Documento: {id_tipo_documento}, Valor Documento: {valor_documento},  Fecha Nacimiento: {fecha_nacimiento}, ID Puesto: {id_puesto}, ID Departamento: {id_departamento}")
              
        id_usuario = request.session.get("_auth_user_id")
        ip_usuario = request.session.get("_auth_user_ip")

        try:
            #Asegurar la conexion
            connection.ensure_connection()
            conn = connection.connection

            conn.execute(
                "EXEC dbo.Sp_InsertarEmpleado ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?",
                [id_usuario, ip_usuario, username, password, int(tipo_usuario), 
                 nombre, int(id_tipo_documento), valor_documento, 
                 fecha_nacimiento, int(id_puesto), int(id_departamento)]
            )

            # Si no hay excepción, devolvemos JSON de éxito
            return JsonResponse({"success": True, "mensaje": "Empleado insertado correctamente"})

        except Exception as e:
            # Capturar cualquier error que lance el THROW del SP
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    # Si no es POST AJAX
    return JsonResponse({"success": False, "error": "Método no permitido."}, status=400)