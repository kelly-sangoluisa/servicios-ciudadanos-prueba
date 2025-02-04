"""
Modelo que gestiona los registros de asistencia a eventos municipales.
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano

class EstadoRegistroAsistencia:
    """Constantes para los estados de registro de asistencia"""
    INSCRITO = 'INSCRITO'
    EN_ESPERA = 'EN_ESPERA'
    CANCELADO = 'CANCELADO'
    ASISTIO = 'ASISTIO'
    NO_ASISTIO = 'NO_ASISTIO'

    CHOICES = [
        (INSCRITO, 'Inscrito'),
        (EN_ESPERA, 'En Lista de Espera'),
        (CANCELADO, 'Cancelado'),
        (ASISTIO, 'Asistió'),
        (NO_ASISTIO, 'No Asistió'),
    ]

    ESTADOS_ACTIVOS = [INSCRITO, EN_ESPERA]

class RegistroAsistenciaQuerySet(models.QuerySet):
    """QuerySet personalizado para consultas comunes de RegistroAsistencia"""

    def activos(self):
        """Obtiene todos los registros activos"""
        return self.filter(estado_registro__in=EstadoRegistroAsistencia.ESTADOS_ACTIVOS)

    def inscritos(self):
        """Obtiene todos los registros con estado inscrito"""
        return self.filter(estado_registro=EstadoRegistroAsistencia.INSCRITO)

    def en_espera(self):
        """Obtiene todos los registros en lista de espera"""
        return self.filter(estado_registro=EstadoRegistroAsistencia.EN_ESPERA)

class RegistroAsistenciaManager(models.Manager):
    """Manager personalizado para consultas comunes de RegistroAsistencia"""
    
    def get_queryset(self):
        """Retorna el queryset personalizado"""
        return RegistroAsistenciaQuerySet(self.model, using=self._db)
    
    def inscritos_para_ciudadano(self, ciudadano):
        """Obtiene todos los registros activos de un ciudadano"""
        return self.get_queryset().filter(
            ciudadano=ciudadano,
            estado_registro=EstadoRegistroAsistencia.INSCRITO
        )
    
    def en_espera_para_ciudadano(self, ciudadano):
        """Obtiene todos los registros en lista de espera de un ciudadano"""
        return self.get_queryset().filter(
            ciudadano=ciudadano,
            estado_registro=EstadoRegistroAsistencia.EN_ESPERA
        )
    
    def obtener_siguiente_en_espera(self, evento):
        """Obtiene el siguiente registro en lista de espera para un evento"""
        return self.get_queryset().filter(
            evento=evento,
            estado_registro=EstadoRegistroAsistencia.EN_ESPERA
        ).order_by('fecha_inscripcion').first()

    def tiene_inscripcion_activa(self, evento, ciudadano):
        """Verifica si un ciudadano tiene una inscripción activa en un evento"""
        return self.get_queryset().filter(
            evento=evento,
            ciudadano=ciudadano,
            estado_registro__in=EstadoRegistroAsistencia.ESTADOS_ACTIVOS
        ).exists()

class RegistroAsistencia(models.Model):
    """
    Modelo que gestiona las inscripciones de ciudadanos a eventos municipales.
    Maneja estados de inscripción y lista de espera.
    """

    # Usar las constantes de EstadoRegistroAsistencia
    ESTADO_INSCRITO = EstadoRegistroAsistencia.INSCRITO
    ESTADO_EN_ESPERA = EstadoRegistroAsistencia.EN_ESPERA
    ESTADO_CANCELADO = EstadoRegistroAsistencia.CANCELADO
    ESTADO_ASISTIO = EstadoRegistroAsistencia.ASISTIO
    ESTADO_NO_ASISTIO = EstadoRegistroAsistencia.NO_ASISTIO
    
    ESTADOS_REGISTRO = EstadoRegistroAsistencia.CHOICES

    ciudadano = models.ForeignKey(
        Ciudadano,
        on_delete=models.CASCADE,
        verbose_name='Ciudadano',
        help_text='Ciudadano que se inscribe al evento'
    )
    
    evento = models.ForeignKey(
        'entidad_municipal_app.EventoMunicipal',  # Referencia lazy para evitar importación circular
        on_delete=models.CASCADE,
        verbose_name='Evento',
        help_text='Evento al que se inscribe el ciudadano'
    )
    
    estado_registro = models.CharField(
        max_length=20,
        choices=ESTADOS_REGISTRO,
        verbose_name='Estado del Registro',
        help_text='Estado actual de la inscripción'
    )
    
    fecha_inscripcion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Inscripción',
        help_text='Fecha y hora en que se realizó la inscripción'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Modificación',
        help_text='Fecha y hora de la última modificación'
    )

    objects = RegistroAsistenciaManager()

    class Meta:
        verbose_name = 'Registro de Asistencia'
        verbose_name_plural = 'Registros de Asistencia'
        unique_together = ['ciudadano', 'evento']
        ordering = ['fecha_inscripcion']
        indexes = [
            models.Index(fields=['estado_registro']),
            models.Index(fields=['fecha_inscripcion']),
        ]

    def clean(self):
        """Validaciones personalizadas del modelo"""
        if self.estado_registro not in dict(self.ESTADOS_REGISTRO):
            raise ValidationError({
                'estado_registro': f'Estado de registro no válido: {self.estado_registro}'
            })

    def save(self, *args, **kwargs):
        """Guarda el registro después de validarlo"""
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def esta_activo(self):
        """Verifica si la inscripción está en un estado activo"""
        return self.estado_registro in EstadoRegistroAsistencia.ESTADOS_ACTIVOS

    def actualizar_estado(self, nuevo_estado):
        """
        Actualiza el estado del registro de asistencia.
        
        Args:
            nuevo_estado: Nuevo estado a establecer.
            
        Raises:
            ValidationError: Si el estado no es válido o la transición no está permitida.
        """
        if nuevo_estado not in dict(self.ESTADOS_REGISTRO):
            raise ValidationError({
                'estado_registro': f'Estado no válido: {nuevo_estado}'
            })

        # Definir transiciones permitidas
        transiciones_validas = {
            self.ESTADO_INSCRITO: [self.ESTADO_EN_ESPERA, self.ESTADO_CANCELADO],
            self.ESTADO_EN_ESPERA: [self.ESTADO_INSCRITO, self.ESTADO_CANCELADO],
            self.ESTADO_CANCELADO: [],  # No se permite cambiar desde cancelado
            self.ESTADO_ASISTIO: [],    # No se permite cambiar desde asistió
            self.ESTADO_NO_ASISTIO: [], # No se permite cambiar desde no asistió
        }
        
        # Validar la transición
        if nuevo_estado not in transiciones_validas.get(self.estado_registro, []):
            raise ValidationError({
                'estado_registro': f'No se permite cambiar de {self.estado_registro} a {nuevo_estado}'
            })
        
        # Guardar el estado anterior para notificaciones
        estado_anterior = self.estado_registro
        
        # Actualizar estado
        self.estado_registro = nuevo_estado
        self.save()
        
        # Si el cambio fue significativo, notificar al ciudadano
        if estado_anterior != nuevo_estado:
            self.evento._enviar_notificacion_inscripcion(self)

    def obtener_formato_fecha_inscripcion(self):
        """Retorna la fecha de inscripción en formato legible"""
        return self.fecha_inscripcion.strftime('%d/%m/%Y %H:%M')

    def __str__(self):
        """Representación en string del registro"""
        return (
            f"{self.ciudadano.obtener_nombre_completo()} - "
            f"{self.evento.nombre_evento} ({self.estado_registro})"
        )
