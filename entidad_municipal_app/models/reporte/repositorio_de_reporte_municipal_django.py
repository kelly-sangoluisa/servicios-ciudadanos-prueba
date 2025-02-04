# entidad_municipal_app/models/reporte/repositorio_de_reporte_municipal_django.py
from django.db import transaction
from .repositorio_de_reporte_municipal import RepositorioDeReporteMunicipal
from .reporte_municipal import ReporteMunicipal


class RepositorioDeReporteMunicipalDjango(RepositorioDeReporteMunicipal):
    """
    Implementación de Django del repositorio de reportes municipales.
    """

    def obtener_por_id(self, id_reporte: int):
        """
        Obtiene un reporte municipal por su ID usando Django ORM.
        """
        try:
            return ReporteMunicipal.objects.get(id=id_reporte)
        except ReporteMunicipal.DoesNotExist:
            return None

    def obtener_todos(self):
        """
        Obtiene todos los reportes municipales usando Django ORM.
        """
        return list(ReporteMunicipal.objects.all())

    def obtener_por_estado(self, estado: str):
        """
        Obtiene reportes municipales por estado usando Django ORM.
        """
        return list(ReporteMunicipal.objects.filter(estado=estado))

    @transaction.atomic
    def crear(self, reporte_ciudadano):
        """
        Crea un nuevo reporte municipal usando Django ORM.
        """
        reporte_municipal = ReporteMunicipal.objects.create(
            reporte_ciudadano=reporte_ciudadano,
            estado="asignado",
            evidencia=None
        )
        reporte_municipal.save()
        return reporte_municipal

    @transaction.atomic
    def actualizar(self, reporte_municipal):
        """
        Actualiza un reporte municipal usando Django ORM.
        """
        reporte_municipal.save()
        return reporte_municipal

    def eliminar(self, id_reporte: int):
        """
        Elimina un reporte municipal usando Django ORM.
        """
        try:
            reporte = ReporteMunicipal.objects.get(id=id_reporte)
            reporte.delete()
            return True
        except ReporteMunicipal.DoesNotExist:
            return False
