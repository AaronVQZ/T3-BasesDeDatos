from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json



# Create your views here.
def home(request):

    #search_query = request.GET.get("search", '')
    print("hereiam")
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
        
        empleados = conn.execute("""
                EXEC Sp_BuscarEmpleado 
                @InSearchTerm = ?,
                @InIdUsuario = ?,
                @InIpUsuario = ?;
                """,(search_term, int(id_usuario), str(ip_usuario))).fetchall()
        
        print("Empleados obtenidos:", empleados)
        # Se convierten los resultados a una lista de diccionarios
        empleados_list = [{'nombre': row[0],'puesto': row[1],} for row in empleados]
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

