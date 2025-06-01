# mi_app/management/commands/cargar_catalogos.py

import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection

class Command(BaseCommand):
    help = "Carga los catálogos desde el XML a la base de datos (invoca SpCargarCatalogos sin usar cursores)"

    def handle(self, *args, **options):
        # 1) Leer el XML desde la carpeta 'datos/'
        base_dir = settings.BASE_DIR
        xml_path = os.path.join(base_dir, "datos", "catalogos.xml")

        try:
            with open(xml_path, "r", encoding="utf-8") as f:
                xml_content = f.read()
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Archivo no encontrado: {xml_path}"))
            return

        # Quitar la cabecera <?xml ...?> si existe
        xml_content = re.sub(r"<\?xml[^>]*\?>\s*", "", xml_content).strip()

        # 2) Asegurarnos de que la conexión esté abierta
        connection.ensure_connection()
        conn = connection.connection  # objeto DBAPI (pyodbc, pymssql, etc.)

        try:
            # 3) Ejecutar el Stored Procedure usando conn.execute()
            sql = """
            DECLARE @outCode INT;
            EXEC dbo.SpCargarCatalogos 
                @inXmlData = ?,
                @outResultCode = @outCode OUTPUT;
            SELECT @outCode;
            """
            # Pasamos xml_content como parámetro (placeholder '?' para pyodbc/pymssql)
            cursor_obj = conn.execute(sql, xml_content)

            # 4) Leer un registro del resultado
            row = cursor_obj.fetchone()
            out_code = row[0] if row else None

            # 5) Cerrar el objeto cursor
            cursor_obj.close()

            if out_code == 0:
                self.stdout.write(self.style.SUCCESS("Catálogos cargados con éxito."))
            else:
                self.stderr.write(self.style.ERROR(f"Error al cargar catálogos (código {out_code})."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Fallo al ejecutar SpCargarCatalogos: {e}"))

