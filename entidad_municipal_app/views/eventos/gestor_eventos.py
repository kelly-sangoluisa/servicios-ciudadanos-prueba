from django.shortcuts import render
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required

@entidad_required
def gestor_eventos(request):
    """Vista para listar todos los eventos activos."""
    # Filtrar eventos por la entidad municipal del usuario autenticado
    entidad_municipal = request.user
    eventos = EventoMunicipal.objects.filter(entidad_municipal=entidad_municipal)
    return render(request, 'entidad/eventos/gestor_eventos.html', {'eventos': eventos})