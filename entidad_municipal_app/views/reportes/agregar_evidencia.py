from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from entidad_municipal_app.decorators import entidad_required
from entidad_municipal_app.models.reporte.repositorio_de_reporte_municipal_django import \
    RepositorioDeReporteMunicipalDjango
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal

@entidad_required
def agregar_evidencia(request, reporte_id):
    repositorio = RepositorioDeReporteMunicipalDjango()
    servicio_reporte = ServicioReporteMunicipal(repositorio)

    reporte = servicio_reporte.obtener_reporte_municipal_por_id(reporte_id)

    if not reporte:
        messages.error(request, "Reporte no encontrado.")
        return redirect('lista_todos_reportes')

    # Manejar la solicitud POST
    if request.method == 'POST':
        comentario = request.POST.get('comentario', '').strip()
        if not comentario:
            messages.error(request, "El comentario es obligatorio para resolver el reporte.")
        else:
            # Registrar la evidencia y cambiar el estado a 'resuelto'
            try:
                servicio_reporte.registrar_evidencia(reporte, comentario)
                messages.success(request, "El reporte ha sido resuelto exitosamente.")
            except Exception as e:
                print(f"Error {e}")
                messages.error(request, "La evidencia no pudo ser registrada.")
            return redirect('lista_todos_reportes')

    return render(request, 'entidad/reportes/resolver_reporte.html', {'reporte': reporte})
