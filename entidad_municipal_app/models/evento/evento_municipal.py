"""
Modelo que representa un evento municipal.
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from .registro_asistencia import RegistroAsistencia

class ErrorGestionEventos(Exception):
    """Excepción personalizada para errores en la gestión de eventos"""
    pass

class EventoMunicipalManager(models.Manager):
    def crear_evento_con_aforo(self, nombre, descripcion, fecha, lugar, capacidad, entidad_municipal, espacio_publico=None):
        if espacio_publico:
            lugar = espacio_publico.direccion
            espacio_publico.estado_espacio_publico = espacio_publico.ESTADO_NO_DISPONIBLE
            espacio_publico.save()

        return self.create(
            nombre_evento=nombre,
            descripcion_evento=descripcion,
            fecha_realizacion=fecha,
            lugar_evento=lugar,
            capacidad_maxima=capacidad,
            estado_actual=self.model.ESTADO_PROGRAMADO,
            espacio_publico=espacio_publico,  # Asignar el espacio público si se proporciona
            entidad_municipal=entidad_municipal  # Asignar la entidad municipal
        )

class EventoMunicipal(models.Model):
    """
    Modelo que representa un evento organizado por la entidad municipal.
    Gestiona el aforo y estado del evento.
    """

    ESTADO_PROGRAMADO = 'PROGRAMADO'
    ESTADO_EN_CURSO = 'EN_CURSO'
    ESTADO_FINALIZADO = 'FINALIZADO'
    ESTADO_CANCELADO = 'CANCELADO'

    ESTADOS_EVENTO = [
        (ESTADO_PROGRAMADO, 'Programado'),
        (ESTADO_EN_CURSO, 'En Curso'),
        (ESTADO_FINALIZADO, 'Finalizado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    # Estados de registro (copiados de RegistroAsistencia para evitar importación circular)
    ESTADO_INSCRITO = 'INSCRITO'
    ESTADO_EN_ESPERA = 'EN_ESPERA'
    ESTADO_CANCELADO_REGISTRO = 'CANCELADO'
    ESTADO_ASISTIO = 'ASISTIO'
    ESTADO_NO_ASISTIO = 'NO_ASISTIO'

    nombre_evento = models.CharField(
        max_length=200,
        verbose_name='Nombre del Evento',
        help_text='Nombre descriptivo del evento municipal'
    )

    descripcion_evento = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada del evento'
    )

    fecha_realizacion = models.DateTimeField(
        verbose_name='Fecha de Realización',
        help_text='Fecha y hora en que se realizará el evento'
    )

    lugar_evento = models.CharField(
        max_length=200,
        verbose_name='Lugar',
        help_text='Ubicación donde se realizará el evento'
    )

    capacidad_maxima = models.PositiveIntegerField(
        verbose_name='Capacidad Máxima',
        help_text='Número máximo de personas que pueden asistir'
    )

    estado_actual = models.CharField(
        max_length=20,
        choices=ESTADOS_EVENTO,
        default=ESTADO_PROGRAMADO,
        verbose_name='Estado del Evento',
        help_text='Estado actual del evento'
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación',
        help_text='Fecha y hora en que se creó el registro del evento'
    )

    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización',
        help_text='Fecha y hora de la última modificación'
    )

    espacio_publico = models.ForeignKey(
        'entidad_municipal_app.EspacioPublico',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='eventos',
        verbose_name='Espacio Público',
        help_text='Espacio público donde se realizará el evento'
    )

    entidad_municipal = models.ForeignKey(
        'entidad_municipal_app.EntidadMunicipal',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='entidad',
        verbose_name='Entidad Municipal',
        help_text='Entidad municipal que organiza el evento'
    )

    motivo_cancelacion = models.TextField(
        max_length=200,
        blank=True,
        default= "",
        verbose_name='Motivo de Cancelación',
        help_text='Razón por la que se canceló el evento'
    )

    def set_motivo_cancelacion(self, motivo):
        self.motivo_cancelacion = motivo
        self.save()


    objects = EventoMunicipalManager()

    class Meta:
        verbose_name = 'Evento Municipal'
        verbose_name_plural = 'Eventos Municipales'
        ordering = ['-fecha_realizacion']

    @property
    def cupos_disponibles(self):
        """
        Calcula los cupos disponibles del evento de forma atómica
        """
        return self.capacidad_maxima - self.registroasistencia_set.filter(
            estado_registro=self.ESTADO_INSCRITO
        ).count()

    def _get_cupos_ocupados(self):
        """Obtiene el número de cupos ocupados"""
        return self.registroasistencia_set.filter(
            estado_registro=self.ESTADO_INSCRITO
        ).count()

    def reducir_cupo_disponible(self):
        """
        Reduce el cupo disponible de forma segura con manejo de concurrencia

        Returns:
            bool: True si se pudo reducir el cupo, False si no hay cupos disponibles
        """
        with transaction.atomic():
            # Bloquea el registro para operaciones concurrentes
            evento = EventoMunicipal.objects.select_for_update().get(pk=self.pk)
            if evento.cupos_disponibles > 0:
                return True
            return False

    def aumentar_cupo_disponible(self):
        """
        Aumenta el cupo disponible de forma segura con manejo de concurrencia

        Returns:
            bool: True si se pudo aumentar el cupo, False si no se pudo aumentar
        """
        with transaction.atomic():
            # Bloquea el registro para operaciones concurrentes
            evento = EventoMunicipal.objects.select_for_update().get(pk=self.pk)
            if evento.capacidad_maxima > evento._get_cupos_ocupados():
                return True
            return False

    def esta_disponible_para_inscripcion(self):
        """
        Verifica si el evento está disponible para inscripciones

        Returns:
            bool: True si el evento está disponible para inscripciones
        """
        return (
            self.estado_actual == self.ESTADO_PROGRAMADO and
            self.fecha_realizacion > timezone.now() and
            self.cupos_disponibles > 0
        )

    def obtener_inscritos(self):
        """
        Obtiene la lista de ciudadanos inscritos al evento

        Returns:
            QuerySet: QuerySet de RegistroAsistencia con estado INSCRITO
        """
        return self.registroasistencia_set.filter(
            estado_registro=self.ESTADO_INSCRITO
        ).select_related('ciudadano')

    def obtener_lista_espera(self):
        """
        Obtiene la lista de espera ordenada por fecha de inscripción

        Returns:
            QuerySet: QuerySet de RegistroAsistencia con estado EN_ESPERA
        """
        return self.registroasistencia_set.filter(
            estado_registro=self.ESTADO_EN_ESPERA
        ).select_related('ciudadano').order_by('fecha_inscripcion')

    def obtener_formato_fecha(self):
        """Retorna la fecha del evento en formato legible"""
        return self.fecha_realizacion.strftime("%d/%m/%Y %H:%M")

    def obtener_todos_registros(self):
        """
        Obtiene todos los registros de asistencia del evento.

        Returns:
            QuerySet: QuerySet de RegistroAsistencia con todos los estados
        """
        return self.registroasistencia_set.all().select_related('ciudadano')

    @transaction.atomic
    def actualizar_estado_asistencia(self, registro_id, nuevo_estado):
        """
        Actualiza el estado de asistencia de un registro.

        Args:
            registro_id: ID del registro a actualizar
            nuevo_estado: Nuevo estado a asignar

        Returns:
            RegistroAsistencia: Registro actualizado

        Raises:
            ErrorGestionEventos: Si hay problemas con la actualización
        """
        try:
            registro = self.registroasistencia_set.select_for_update().get(id=registro_id)
            estados_validos = [
                self.ESTADO_INSCRITO,
                self.ESTADO_EN_ESPERA,
                self.ESTADO_ASISTIO,
                self.ESTADO_NO_ASISTIO,
                self.ESTADO_CANCELADO_REGISTRO
            ]
            
            if nuevo_estado not in estados_validos:
                raise ErrorGestionEventos(f"Estado no válido: {nuevo_estado}")
                
            registro.estado_registro = nuevo_estado
            registro.save()
            return registro
            
        except RegistroAsistencia.DoesNotExist:
            raise ErrorGestionEventos("Registro de asistencia no encontrado")

    def save(self, *args, **kwargs):
        # Si el evento tiene un espacio público asociado, actualiza el lugar_evento
        if self.espacio_publico:
            self.lugar_evento = self.espacio_publico.direccion
        super().save(*args, **kwargs)

    @transaction.atomic
    def inscribir_ciudadano(self, ciudadano):
        """
        Inscribe a un ciudadano en el evento o reactiva una inscripción cancelada.

        Args:
            ciudadano: Instancia del ciudadano a inscribir

        Returns:
            RegistroAsistencia: Registro creado o actualizado

        Raises:
            ErrorGestionEventos: Si hay problemas con la inscripción
        """
        # Obtener y bloquear el evento para operaciones concurrentes
        evento = EventoMunicipal.objects.select_for_update().get(pk=self.pk)

        try:
            # Intentar obtener un registro existente para este ciudadano y evento
            registro_existente = RegistroAsistencia.objects.get(ciudadano=ciudadano, evento=evento)
            
            # Si el registro está activo, no permitir reinscripción
            if registro_existente.estado_registro in [RegistroAsistencia.ESTADO_INSCRITO, RegistroAsistencia.ESTADO_EN_ESPERA]:
                raise ErrorGestionEventos("Ya tienes una inscripción activa para este evento")
            
            # Si el registro está cancelado, reactivarlo
            if registro_existente.estado_registro == RegistroAsistencia.ESTADO_CANCELADO:
                nuevo_estado = (
                    RegistroAsistencia.ESTADO_INSCRITO
                    if evento.esta_disponible_para_inscripcion() and evento.cupos_disponibles > 0
                    else RegistroAsistencia.ESTADO_EN_ESPERA
                )
                registro_existente.estado_registro = nuevo_estado
                registro_existente.save()
                self._enviar_notificacion_inscripcion(registro_existente)
                return registro_existente

        except RegistroAsistencia.DoesNotExist:
            # No existe registro previo, crear uno nuevo
            nuevo_estado = (
                RegistroAsistencia.ESTADO_INSCRITO
                if evento.esta_disponible_para_inscripcion() and evento.cupos_disponibles > 0
                else RegistroAsistencia.ESTADO_EN_ESPERA
            )
            registro = RegistroAsistencia.objects.create(
                ciudadano=ciudadano,
                evento=evento,
                estado_registro=nuevo_estado
            )
            self._enviar_notificacion_inscripcion(registro)
            return registro

    @transaction.atomic
    def cancelar_inscripcion(self, registro_id):
        """
        Cancela una inscripción y maneja la lista de espera

        Args:
            registro_id: ID del registro a cancelar

        Returns:
            tuple: (registro_cancelado, registro_promovido)

        Raises:
            ErrorGestionEventos: Si hay problemas con la cancelación
        """
        try:
            registro = RegistroAsistencia.objects.select_related('evento').get(pk=registro_id)

            if registro.evento_id != self.pk:
                raise ErrorGestionEventos("El registro no pertenece a este evento")

            if registro.estado_registro == RegistroAsistencia.ESTADO_CANCELADO:
                raise ErrorGestionEventos("El registro ya está cancelado")

            estado_original = registro.estado_registro

            # Cancelar el registro
            registro.actualizar_estado(RegistroAsistencia.ESTADO_CANCELADO)

            # Si estaba inscrito, liberar cupo y promover siguiente
            registro_promovido = None
            if estado_original == RegistroAsistencia.ESTADO_INSCRITO:
                self.aumentar_cupo_disponible()
                registro_promovido = self._promover_siguiente_en_espera()

            # Enviar notificaciones
            self._enviar_notificacion_inscripcion(registro)
            if registro_promovido:
                self._enviar_notificacion_inscripcion(registro_promovido)

            return registro, registro_promovido

        except RegistroAsistencia.DoesNotExist:
            raise ErrorGestionEventos("El registro especificado no existe")

    def _promover_siguiente_en_espera(self):
        """
        Promueve al siguiente ciudadano en lista de espera

        Returns:
            Optional[RegistroAsistencia]: Registro promovido si existe
        """
        siguiente = RegistroAsistencia.objects.obtener_siguiente_en_espera(self)
        if siguiente:
            siguiente.actualizar_estado(RegistroAsistencia.ESTADO_INSCRITO)
            return siguiente
        return None

    def _enviar_notificacion_inscripcion(self, registro):
        """
        Envía una notificación por correo sobre el estado de la inscripción

        Args:
            registro: Instancia de RegistroAsistencia con la información
        """
        plantillas_mensajes = {
            RegistroAsistencia.ESTADO_INSCRITO: {
                'asunto': 'Confirmación de inscripción',
                'mensaje': 'Tu inscripción ha sido confirmada'
            },
            RegistroAsistencia.ESTADO_EN_ESPERA: {
                'asunto': 'Agregado a lista de espera',
                'mensaje': 'Has sido agregado a la lista de espera'
            },
            RegistroAsistencia.ESTADO_CANCELADO: {
                'asunto': 'Cancelación de inscripción',
                'mensaje': 'Tu inscripción ha sido cancelada'
            },
        }

        plantilla = plantillas_mensajes.get(
            registro.estado_registro,
            {
                'asunto': 'Actualización de registro',
                'mensaje': 'Ha habido una actualización en tu registro'
            }
        )

        asunto = f'{plantilla["asunto"]} - {self.nombre_evento}'
        mensaje = f'''
        Hola {registro.ciudadano.obtener_nombre_completo()},

        {plantilla["mensaje"]} para el evento "{self.nombre_evento}".
        
        Detalles del evento:
        - Fecha: {self.obtener_formato_fecha()}
        - Lugar: {self.lugar_evento}
        - Estado de tu registro: {registro.estado_registro}
        
        Gracias por tu interés en nuestros eventos municipales.
        '''

        try:
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[registro.ciudadano.correo_electronico],
                fail_silently=False
            )
        except Exception as e:
            # Log the error but don't stop the process
            print(f"Error al enviar notificación: {str(e)}")

    def validar_estado_actual(self,estado_actual):
        if estado_actual == self.ESTADO_CANCELADO:
            raise ValidationError("El evento ya ha sido cancelado")
        return True

    def __str__(self):
        return f"{self.nombre_evento} ({self.obtener_formato_fecha()})"
