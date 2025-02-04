from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo

@login_required
def suscribirse_canal(request, canal_id):
    """
        Permite que un ciudadano se suscriba a un canal informativo.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            canal_id (int): El identificador del canal informativo al que el usuario desea suscribirse.

        Returns:
            HttpResponseRedirect: Redirige a la página previa o al dashboard del ciudadano.

        Raises:
            CanalInformativo.DoesNotExist: Si el canal con el ID proporcionado no existe.
            Ciudadano.DoesNotExist: Si no se encuentra un ciudadano con el ID del usuario autenticado.
    """
    canal = CanalInformativo.objects.get(id=canal_id)
    ciudadano = Ciudadano.objects.get(id=request.user.id)
    canal.suscribir_ciudadano(ciudadano)
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_ciudadano'))

@login_required
def desuscribirse_canal(request, canal_id):
    """
        Permite que un ciudadano se desuscriba de un canal informativo.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            canal_id (int): El identificador del canal informativo del que el usuario desea desuscribirse.

        Returns:
            HttpResponseRedirect: Redirige a la página previa o al dashboard del ciudadano.

        Raises:
            CanalInformativo.DoesNotExist: Si el canal con el ID proporcionado no existe.
            Ciudadano.DoesNotExist: Si no se encuentra un ciudadano con el ID del usuario autenticado.
            ValueError: Si la desuscripción no es posible.
    """
    canal = CanalInformativo.objects.get(id=canal_id)
    ciudadano = Ciudadano.objects.get(id=request.user.id)
    try:
        canal.desuscribir_ciudadano(ciudadano)
    except ValueError as e:
        # Manejar el caso en que la desuscripción no sea posible
        pass
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_ciudadano'))
