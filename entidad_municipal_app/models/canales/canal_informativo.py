from django.db import models
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from django.utils.timezone import now

from entidad_municipal_app.models import EntidadMunicipal
from shared.models.notificacion.notificacion import Notificacion


class CanalInformativo(models.Model):
    """
    Representa un canal general de noticias o información.

    Este modelo gestiona canales a los cuales los ciudadanos pueden suscribirse para recibir noticias o alertas.
    Puede ser un canal informativo o un canal de emergencia.
    Los ciudadanos pueden ser notificados de nuevas noticias, y se gestionan las suscripciones a los canales.

    Attributes:
        nombre (str): El nombre único del canal.
        descripcion (str): Una descripción del canal.
        es_emergencia (bool): Indicador de si el canal es de emergencia. Por defecto es False.
    """
    entidad_municipal = models.ForeignKey(EntidadMunicipal, on_delete=models.CASCADE, related_name="canales", null=True)
    nombre = models.CharField(max_length=255, unique=True)
    descripcion = models.TextField()
    es_emergencia = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Canal Informativo"
        verbose_name_plural = "Canales Informativos"

    def __str__(self):
        """
        Retorna el nombre del canal.

        Returns:
            str: El nombre del canal.
        """
        return self.nombre

    def suscribir_ciudadano(self, ciudadano):
        """
        Suscribe al ciudadano al canal.

        Si el ciudadano no está ya suscrito, se crea la suscripción.

        Args:
            ciudadano (Ciudadano): El ciudadano que se suscribe al canal.
        """
        Suscripcion.objects.get_or_create(canal=self, ciudadano=ciudadano)

    def desuscribir_ciudadano(self, ciudadano):
        """
        Elimina la suscripción del ciudadano al canal.

        Si el canal es de emergencia, no permite la desuscripción.

        Args:
            ciudadano (Ciudadano): El ciudadano que se desea desuscribir.

        Raises:
            ValueError: Si el canal es de emergencia o si el ciudadano no está suscrito.
        """
        if self.es_emergencia:
            raise ValueError("No es posible desuscribirse de un canal de emergencia.")

        try:
            suscripcion = Suscripcion.objects.get(canal=self, ciudadano=ciudadano)
            suscripcion.delete()
        except Suscripcion.DoesNotExist:
            raise ValueError(f"El ciudadano {ciudadano.nombre_completo} no está suscrito al canal {self.nombre}")

    def notificar_noticia(self, noticia):
        """
        Notifica una noticia a todos los ciudadanos suscritos al canal informativo.

        Si el canal es de emergencia, debe utilizarse el método `notificar_alerta_emergencia`.

        Args:
            noticia (Noticia): La noticia que se va a enviar a los suscriptores.

        Raises:
            ValueError: Si se intenta notificar una noticia desde un canal de emergencia.
        """
        if self.es_emergencia:
            raise ValueError("Utiliza notificar_alerta_emergencia para enviar alertas de emergencia.")
        suscripciones = Suscripcion.objects.filter(canal=self)
        for suscripcion in suscripciones.ciudadano:
            Notificacion.objects.create(
                ciudadano=suscripcion.ciudadano,
                titulo=noticia.titulo,
                mensaje=noticia.contenido
            )

    def notificar_alerta_emergencia(self, tipo_incidente, localidad):
        """
    Envía una alerta de emergencia solo a los ciudadanos de una localidad específica.

    Este método solo puede ser utilizado en canales de emergencia.

    Args:
        tipo_incidente (str): El tipo de incidente (ej. "Incendio", "Accidente").
        localidad (str): La localidad donde ocurrió el incidente.

    Raises:
        ValueError: Si el canal no es de emergencia.
    """
        if not self.es_emergencia:
            raise ValueError("Este método solo es válido para canales de emergencia.")

        suscripciones = Suscripcion.objects.filter(canal=self)
        for suscripcion in suscripciones:
            Notificacion.objects.create(
                ciudadano=suscripcion.ciudadano,
                titulo="Alerta de emergencia",
                mensaje=f"Ha ocurrido un {tipo_incidente} en {localidad}"
            )


class Suscripcion(models.Model):
    """
    Relación entre ciudadanos y canales informativos (no de emergencia).

    Este modelo gestiona la suscripción de los ciudadanos a los canales informativos, permitiendo la
    asociación entre un ciudadano y un canal.

    Attributes:
        ciudadano (ForeignKey): El ciudadano suscrito al canal.
        canal (ForeignKey): El canal al que está suscrito el ciudadano.
        fecha_suscripcion (DateTimeField): La fecha y hora en que el ciudadano se suscribe.
    """
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE, related_name="suscripciones")
    canal = models.ForeignKey(CanalInformativo, on_delete=models.CASCADE, related_name="suscripciones")
    fecha_suscripcion = models.DateTimeField(default=now)

    class Meta:
        unique_together = ('ciudadano', 'canal')
        verbose_name = "Suscripción"
        verbose_name_plural = "Suscripciones"

    def __str__(self):
        """
        Retorna un string representando la suscripción.

        Returns:
            str: Representación de la suscripción, indicando el nombre del ciudadano y el canal.
        """
        return f"{self.ciudadano.nombre_completo} suscrito a {self.canal.nombre}"
