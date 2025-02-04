from django.db import models
from django.utils.translation import gettext_lazy as _


class EspacioPublico(models.Model):
    """
    Modelo para representar un espacio público.
    """
    nombre = models.CharField(
        max_length=255,
        help_text="Nombre del espacio público",
        default="Espacio Público"
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name='Lugar',
        help_text='Ubicación donde se encuentra el espacio público'
    )
    descripcion = models.TextField()

    # Corregir la referencia a EntidadMunicipal usando string
    entidad_municipal = models.ForeignKey(
        'entidad_municipal_app.EntidadMunicipal',
        on_delete=models.CASCADE,
        verbose_name=_("Entidad Municipal"),
        related_name='espacios_publicos'
    )

    ESTADO_DISPONIBLE = 'DISPONIBLE'
    ESTADO_NO_DISPONIBLE = 'NO_DISPONIBLE'

    ESTADOS_DISPONIBILIDAD = [
        (ESTADO_DISPONIBLE, 'Disponible'),
        (ESTADO_NO_DISPONIBLE, 'No Disponible'),
    ]

    estado_espacio_publico = models.CharField(
        max_length=20,
        choices=ESTADOS_DISPONIBILIDAD,
        default=ESTADO_DISPONIBLE,
        help_text="Estado del espacio público en la fecha especificada"
    )

    AFECTADO = "AFECTADO"
    NO_AFECTADO = "NO_AFECTADO"
    ESTADO_CHOICES = [
        (AFECTADO, 'Afectado'),
        (NO_AFECTADO, 'No Afectado'),
    ]
    estado_incidente_espacio = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=NO_AFECTADO,
        help_text="Estado del espacio público"
    )

    @classmethod
    def obtener_espacios_disponibles(cls, fecha):
        # Importar EventoMunicipal aquí para evitar importaciones circulares
        from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal

        # Filtrar espacios que están disponibles y que no tienen eventos programados en la fecha dada
        eventos_misma_fecha = EventoMunicipal.objects.filter(
            fecha_realizacion=fecha,
            estado_actual__in=[EventoMunicipal.ESTADO_PROGRAMADO, EventoMunicipal.ESTADO_EN_CURSO]
        ).values_list('espacio_publico_id', flat=True)

        # Obtener espacios disponibles
        espacios_disponibles = cls.objects.filter(
            estado_espacio_publico=cls.ESTADO_DISPONIBLE
        ).exclude(pk__in=eventos_misma_fecha)

        return espacios_disponibles