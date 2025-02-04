from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from shared.models.notificacion.notificacion import Notificacion


class ServicioDeNotificacion:
    def notificar(self, ciudadano, mensaje, asunto="Notificación Importante"):
        # Guardar notificación en la base de datos
        notificacion = Notificacion.objects.create(ciudadano=ciudadano, mensaje=mensaje)

        # Enviar correo electrónico si el ciudadano tiene email registrado
        if ciudadano.email:
            self.enviar_correo(ciudadano.email, asunto, mensaje)

        return notificacion

    def notificar_estado_riesgo(self, ciudadano, sector):
        mensaje = f"Atención: El sector {sector.nombre} se encuentra en estado de riesgo."
        asunto = "⚠️ Alerta de Riesgo en tu Sector"
        return self.notificar(ciudadano, mensaje, asunto)

    def notificar_reporte_cercano(self, ciudadano, reporte, distancia):
        mensaje = (f"Aviso: Se ha registrado un reporte con asunto '{reporte.tipo}' "
                   f"a menos de {distancia} kilómetros de su ubicación actual.")
        asunto = "🔔 Nuevo Reporte Cercano"
        return self.notificar(ciudadano, mensaje, asunto)

    def enviar_correo(self, destinatario, asunto, mensaje):
        """Envía una notificación por correo electrónico."""
        remitente = settings.EMAIL_HOST_USER  # Debes configurarlo en settings.py
        email = EmailMultiAlternatives(
            subject=asunto,
            body=mensaje,
            from_email=remitente,
            to=[destinatario]
        )
        email.send()

    class Meta:
        verbose_name = "Servicio de Notificación"
        verbose_name_plural = "Servicios de Notificación"
