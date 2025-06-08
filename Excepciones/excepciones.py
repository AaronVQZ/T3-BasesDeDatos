
class Error(Exception):
    """Clase base para otras excepciones"""
    def __init__(self):
        self.mensaje = self.mensaje_error()
        super().__init__(self.mensaje) #constructor de la clase Exception
    
    def mensaje_error(self):
        mensaje = "Error: desconocido. "
        return mensaje
        """metodo abstracto que comparten todas las excepciones"""

class Error_Login(Error):
    """Error al intentar iniciar sesi[on]."""
    def __init__(self):
        self.mensaje = self.mensaje_error()
        super().__init__(self.mensaje) #constructor de la clase Exception
    
    def mensaje_error(self):
        mensaje = "Error al iniciar sesión: "
        return mensaje

class Error_password(Error_Login):
    """Error con la contraseña."""
    def __init__(self):
        self.mensaje = self.mensaje_error()
        super().__init__(self.mensaje) 
    
    def mensaje_error(self):
        mensaje = super().mensaje_error() + "Contraseña incorrecta. "
        return mensaje

class Error_Usuario(Error_Login):
    """Error con el usuario."""
    def __init__(self):
        self.mensaje = self.mensaje_error()
        super().__init__(self.mensaje) 
    
    def mensaje_error(self):
        mensaje = super().mensaje_error() + "Usuario no encontrado. "
        return mensaje

class Error_obtener_empleados(Error):
    """Error al obtener empleados."""
    def __init__(self):
        self.mensaje = self.mensaje_error()
        super().__init__(self.mensaje) 
    
    def mensaje_error(self):
        mensaje = "Error al obtener empleados"
        return mensaje