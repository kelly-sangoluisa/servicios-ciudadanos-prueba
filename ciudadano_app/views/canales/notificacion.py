from django.shortcuts import render, redirect
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from shared.models.notificacion.notificacion import Notificacion


def listar_notificacion(request):
    """
    Obtiene y lista las notificaciones de un ciudadano autenticado.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.

        Returns:
            HttpResponse: Renderiza la plantilla 'canales/notificaciones.html' con las notificaciones del ciudadano.

        Raises:
            Ciudadano.DoesNotExist: Si no se encuentra un ciudadano con el ID del usuario autenticado.
    """
    ciudadano = Ciudadano.objects.get(id=request.user.id)
    notificaciones = Notificacion.objects.filter(ciudadano=ciudadano)
    return render(request, 'canales/notificaciones.html', {'notificaciones': notificaciones})
