from django.db import models
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from django.utils import timezone
from ciudadano_app.models import Ciudadano

class Notificacion(models.Model):
    """
            Representa una notificación enviada a un ciudadano.

            Este modelo gestiona las notificaciones que se envían a los ciudadanos, que pueden ser de tipo noticia, alerta
            de emergencia, entre otras. Una notificación incluye un título, un mensaje, la fecha de envío y un indicador de
            si ha sido leída o no por el ciudadano.

            Attributes:
                ciudadano (ForeignKey): El ciudadano que recibe la notificación.
                titulo (str): El título de la notificación.
                mensaje (str): El contenido de la notificación.
                fecha_envio (DateTimeField): La fecha y hora en que se envió la notificación.
                leida (bool): Indicador de si la notificación ha sido leída por el ciudadano. Por defecto es False.
    """
    ciudadano = models.ForeignKey(
        'ciudadano_app.Ciudadano',
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    titulo = models.CharField(max_length=255, default="")
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    leida = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha']

    def _str_(self):
        return f"Notificación para {self.ciudadano.nombre_completo}: {self.mensaje[:50]}..."
