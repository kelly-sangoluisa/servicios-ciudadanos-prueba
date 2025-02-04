from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal, ErrorGestionEventos
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia, EstadoRegistroAsistencia
from entidad_municipal_app.decorators import entidad_required

@entidad_required
def evento(request, evento_id):
    """Vista para mostrar el detalle de un evento y el estado de asistencia de los inscritos."""
    try:
        evento = get_object_or_404(EventoMunicipal, id=evento_id)
        
        # Obtener todos los registros activos (no cancelados)
        inscritos = evento.obtener_todos_registros().exclude(
            estado_registro=EstadoRegistroAsistencia.CANCELADO
        )
        
        # Aplicar filtros de búsqueda
        search_query = request.GET.get('search', '')
        if search_query:
            inscritos = inscritos.filter(
                Q(ciudadano__nombre_completo__icontains=search_query) |
                Q(ciudadano__numero_identificacion__icontains=search_query) |
                Q(ciudadano__correo_electronico__icontains=search_query)
            )
        
        # Filtrar por estado
        filter_category = request.GET.get('filter_category', '')
        if filter_category:
            inscritos = inscritos.filter(estado_registro=filter_category)
        
        # Ordenar por fecha de inscripción
        inscritos = inscritos.order_by('fecha_inscripcion')
        
        context = {
            'evento': evento,
            'inscritos': inscritos,
            'filter_category': filter_category,
            'search_query': search_query,
        }
        return render(request, 'entidad/eventos/evento.html', context)
    
    except Exception as e:
        messages.error(request, f"Error al cargar el evento: {str(e)}")
        return redirect('lista_eventos')

@entidad_required
@require_POST
@transaction.atomic
def actualizar_asistencia(request, registro_id):
    """Vista para actualizar el estado de registro entre INSCRITO y EN_ESPERA."""
    try:
        # Bloquear registro y evento para operación atómica
        registro = get_object_or_404(
            RegistroAsistencia.objects.select_for_update(), 
            id=registro_id
        )
        evento = EventoMunicipal.objects.select_for_update().get(id=registro.evento.id)
        nuevo_estado = request.POST.get('nuevo_estado')
        
        # Validaciones de estado
        estados_permitidos = [EstadoRegistroAsistencia.INSCRITO, EstadoRegistroAsistencia.EN_ESPERA]
        if registro.estado_registro not in estados_permitidos:
            raise ErrorGestionEventos("Solo se puede modificar el estado de registros activos")
        
        if nuevo_estado not in estados_permitidos:
            raise ErrorGestionEventos("Estado no válido para actualización")

        # Validar cambio a EN_ESPERA solo si no hay cupos
        if nuevo_estado == EstadoRegistroAsistencia.EN_ESPERA:
            if evento.cupos_disponibles > 0:
                raise ErrorGestionEventos(
                    "No se puede poner en lista de espera cuando hay cupos disponibles. "
                    "Por favor, inscriba al ciudadano directamente."
                )

        # Validar cambio a INSCRITO solo si hay cupos
        elif nuevo_estado == EstadoRegistroAsistencia.INSCRITO:
            inscritos_actuales = evento.registroasistencia_set.filter(
                estado_registro=EstadoRegistroAsistencia.INSCRITO
            ).exclude(id=registro.id).count()
            
            if inscritos_actuales >= evento.capacidad_maxima:
                raise ErrorGestionEventos(
                    "No hay cupos disponibles para inscribir. "
                    "El ciudadano debe permanecer en lista de espera."
                )

        registro.actualizar_estado(nuevo_estado)
        messages.success(
            request, 
            f"Estado actualizado correctamente a: {dict(EstadoRegistroAsistencia.CHOICES)[nuevo_estado]}"
        )
        
    except ErrorGestionEventos as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, f"Error al actualizar estado: {str(e)}")
    
    return redirect('detalle_evento', evento_id=registro.evento.id)

@entidad_required
@require_POST
def eliminar_inscripcion(request, registro_id):
    """Vista para eliminar/cancelar la inscripción de un ciudadano."""
    try:
        registro = get_object_or_404(RegistroAsistencia, id=registro_id)
        evento = registro.evento
        
        evento.cancelar_inscripcion(registro_id)
        messages.success(request, "Inscripción cancelada correctamente")
        
    except ErrorGestionEventos as e:
        messages.error(request, str(e))
    except Exception as e:
        messages.error(request, f"Error al cancelar inscripción: {str(e)}")
    
    return redirect('detalle_evento', evento_id=registro.evento.id)