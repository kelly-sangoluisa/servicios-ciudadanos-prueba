from django.db import models
from django.utils.translation import gettext_lazy as _

# Importación de modelos necesarios desde la aplicación 'ciudadano_app'.
from .tipo_reporte import TipoReporte

class Reporte(models.Model):
    """
    Modelo para representar un reporte realizado por un ciudadano.
    """

    # Relación con el modelo Ciudadano; se elimina el reporte si el ciudadano se elimina.
    ciudadano = models.ForeignKey(
        'ciudadano_app.Ciudadano',  # Referencia como string
        on_delete=models.CASCADE,
        verbose_name=_("Ciudadano")
    )

    # Relación con el modelo TipoReporte; se elimina el reporte si el tipo de reporte se elimina.
    tipo_reporte = models.ForeignKey(TipoReporte, on_delete=models.CASCADE)

    # Campo para almacenar la ubicación asociada al reporte.
    ubicacion = models.CharField(max_length=255)

    # Campo opcional para establecer la prioridad del reporte, puede ser nulo o en blanco.
    prioridad = models.IntegerField(default=None, null=True, blank=True)

    def validar_reporte(self):
        """
        Método para validar la presencia de los campos obligatorios en el reporte.

        Returns:
            bool: True si el reporte tiene todos los campos necesarios, False en caso contrario.
        """
        return bool(self.ciudadano and self.tipo_reporte and self.ubicacion)

    def _str_(self):
        """
        Método para obtener la representación en cadena del reporte, mostrando información relevante.

        Returns:
            str: Cadena que representa el reporte, incluyendo el asunto y el nombre del ciudadano.
        """
        return f"Reporte de {self.tipo_reporte.asunto} por {self.ciudadano.nombre_completo}"

    def algun_metodo(self):
        from ciudadano_app.models import Ciudadano
        # usar Ciudadano aquí