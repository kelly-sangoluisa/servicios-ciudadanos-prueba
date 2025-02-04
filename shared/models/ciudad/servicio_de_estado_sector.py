# entidad_municipal_app/services/servicio_de_estado_sector.py
from datetime import timedelta
from django.utils.timezone import now
from shared.models.ciudad.sector import ESTADOS_SECTOR

class ServicioDeEstadoSector:
    def __init__(self, sector):
        self.sector = sector

    def actualizar_estado(self):
        # Obtener reportes de los últimos 30 días
        reportes = self.sector.reporte_set.filter(fecha_reporte__gte=now() - timedelta(days=30))
        total_reportes = reportes.count()

        # Contadores de reportes según gravedad
        conteo = {"Seguro": 0, "Precaución": 0, "Riesgo": 0}

        for reporte in reportes:
            for estado, palabras_clave in ESTADOS_SECTOR.items():
                if any(palabra in reporte.asunto.lower() for palabra in palabras_clave):
                    conteo[estado] += 1
                    break  # Solo contar en una categoría

        # Lógica para determinar el estado del sector
        if conteo["Riesgo"] >= 3 or total_reportes >= 20:
            self.sector.estado = "Riesgo"
        elif conteo["Precaución"] >= 3 or total_reportes >= 10:
            self.sector.estado = "Precaución"
        else:
            self.sector.estado = "Seguro"

        self.sector.save()