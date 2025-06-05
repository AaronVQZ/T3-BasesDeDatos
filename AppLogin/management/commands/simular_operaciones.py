# simular_operaciones.py

import os
import re
import xml.etree.ElementTree as ET

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection


class Command(BaseCommand):
    help = "Simula día a día las operaciones del XML invocando SpSimularDiaOperacion"

    def handle(self, *args, **options):
        # 1) Leer el XML desde la carpeta 'datos/'
        base_dir = settings.BASE_DIR
        xml_path = os.path.join(base_dir, "datos", "operacion.xml")

        try:
            with open(xml_path, "r", encoding="utf-8") as f:
                raw = f.read()
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Archivo no encontrado: {xml_path}"))
            return

        # 2) Quitar la cabecera <?xml …?> si existe y hacer strip
        xml_text = re.sub(r"<\?xml[^>]*\?>\s*", "", raw).strip()

        # 3) Asegurar la conexión y obtener el objeto DBAPI (pyodbc, pymssql, etc.)
        connection.ensure_connection()
        conn = connection.connection

        # 4) Parsear todo el XML para extraer las fechas (puede haberlas debajo de <Operacion>)
        try:
            # Envolvemos en <root>…</root> para tener un único nodo padre
            root = ET.fromstring(f"<root>{xml_text}</root>")
        except ET.ParseError as e:
            self.stderr.write(self.style.ERROR(f"Error al parsear operacion.xml: {e}"))
            return

        # Ahora buscamos en todo el árbol todos los nodos <FechaOperacion>
        fechas = []
        for elem in root.findall(".//FechaOperacion"):
            fecha_atr = elem.get("Fecha")
            if fecha_atr:
                fechas.append(fecha_atr)

        fechas = sorted(set(fechas))

        if not fechas:
            self.stdout.write(self.style.WARNING("No se encontró ninguna <FechaOperacion> en el XML."))
            return

        success = 0
        errors = 0

        for fecha in fechas:
            try:
                sql = """
                DECLARE @outCode INT;
                EXEC dbo.SpSimularDiaOperacion
                    @FechaOperacion   = ?,
                    @inXmlOperaciones = ?,
                    @OutResultCode    = @outCode OUTPUT;
                SELECT @outCode;
                """
                resultado_sp = conn.execute(sql, fecha, xml_text)
                fila = resultado_sp.fetchone()
                resultado_sp.close()

                out_code = fila[0] if fila else None
                if out_code == 1:
                    self.stdout.write(self.style.SUCCESS(f"[{fecha}] Simulación exitosa."))
                    success += 1
                else:
                    self.stderr.write(self.style.ERROR(f"[{fecha}] SpSimularDiaOperacion devolvió {out_code}"))
                    errors += 1

            except Exception as e:
                errors += 1
                self.stderr.write(self.style.ERROR(f"[{fecha}] Error al invocar SpSimularDiaOperacion: {e}"))

        self.stdout.write(
            self.style.SUCCESS(
                f"Proceso terminado: {success} fechas OK, {errors} con error."
            )
        )
