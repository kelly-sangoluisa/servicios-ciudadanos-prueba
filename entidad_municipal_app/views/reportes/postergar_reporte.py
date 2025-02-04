from django.shortcuts import redirect
from django.contrib import messages

from entidad_municipal_app.decorators import entidad_required
from entidad_municipal_app.models.reporte.repositorio_de_reporte_municipal_django import \
    RepositorioDeReporteMunicipalDjango
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal

@entidad_required
def postergar_reporte(request, reporte_id):
    if request.method == "POST":
        # Inicializar el repositorio y el servicio de reporte municipal
        repositorio = RepositorioDeReporteMunicipalDjango()
        servicio_reporte = ServicioReporteMunicipal(repositorio)

        # Obtener el reporte a través del servicio
        reporte = servicio_reporte.obtener_reporte_municipal_por_id(reporte_id)

        try:
            servicio_reporte.postergar_reporte(reporte_id)
            messages.success(request, f'El reporte #{reporte_id} se ha sido postergado.')
        except Exception as e:
            print(f"Error {e}")
            estado = reporte.obtener_estado()
            messages.error(request, f"No se pudo postergar el reporte ya que está {estado}")

    # Redirigir a la vista de ver reportes
    return redirect('lista_todos_reportes')