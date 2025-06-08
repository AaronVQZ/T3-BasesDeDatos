from django.shortcuts import render
from django.http import JsonResponse
from django.db import connection
import json
from Excepciones import excepciones as excepciones





def login(request):
    if request.method == "POST":
        ip = request.META.get('REMOTE_ADDR')

        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Datos inválidos"}, status=400)

            username = data.get('username', '')
            password = data.get('password', '')
        else:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')

        print(f"Datos recibidos: username={username}, password={password}")

        try:
            connection.ensure_connection()
            conn = connection.connection

            codigo_error = 0
            # Validar usuario
            result = conn.execute(
                    """
                     DECLARE @OutCodigoError INT;
                     EXEC dbo.sp_ValidarUsuario @InUsername = ?, @InPassword = ?, @InIpUsuario = ?, @OutCodigoError = ?
                    """,
                    (username, password, ip, codigo_error)).fetchone()

            es_valido, es_admin, id_usuario, mensaje = result


            print(f"Es válido: {es_valido},Es Administrador {es_admin} Mensaje: {mensaje}")
            print(f"codigo_error: {codigo_error}")

            if codigo_error != 0:
                if codigo_error == 1:
                    raise excepciones.Error_Usuario()
                elif codigo_error == 2:
                    raise excepciones.Error_password()
                else:
                    raise excepciones.Error()

            if es_valido:
                request.session['_auth_user_id'] = id_usuario
                request.session['_auth_user_backend'] = 'django.contrib.auth.backends.ModelBackend'
                request.session['_auth_user_ip'] = ip
                request.user = Usuario(id_usuario=id_usuario, username=username)
                print("ok!")
                # Si el usuario es administrador, redirigir a la página de administración
                if es_admin:
                    request.session['is_admin'] = True
                    return JsonResponse({"success": True, "redirect": "/administrador"})                
                
                # Si el usuario es normal, redirigir a la página de inicio
                else:
                    request.session['is_admin'] = False
                    return JsonResponse({"success": True, "redirect": "/empleado"})

            else:
                return JsonResponse({"error": "invalid_credentials", "message": mensaje}, status=400)

        except Exception as e:
            print(f"Error de base de datos: {str(e)}")
            return JsonResponse({"error": "database_error", "message": str(e)}, status=500)


    # Si no es una solicitud POST, o si no se envían datos, mostrar el formulario de inicio de sesión
    return render(request, "login.html", {"blocked": False})


class Usuario:
    def __init__(self, id_usuario, username):
        self.id_usuario = id_usuario
        self.username = username

    @property
    def valido(self):
        return True

    def username(self):
        return self.username