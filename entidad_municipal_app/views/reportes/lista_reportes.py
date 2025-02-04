from django.shortcuts import render

from entidad_municipal_app.models.departamento.repositorio_departamento_django import RepositorioDepartamentoDjango
from entidad_municipal_app.models.departamento.servicio_departamento import ServicioDepartamento
from entidad_municipal_app.models.reporte.repositorio_de_reporte_municipal_django import \
    RepositorioDeReporteMunicipalDjango
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal


def lista_todos_reportes(request):
    """View to list all municipal reports, filtered by department if selected."""

    repositorio_reportes = RepositorioDeReporteMunicipalDjango()
    repositorio_departamentos = RepositorioDepartamentoDjango()
    servicio_reporte = ServicioReporteMunicipal(repositorio_reportes)
    servicio_departamento = ServicioDepartamento(repositorio_departamentos)

    # Get all reports and departments
    todos_reportes = servicio_reporte.obtener_reportes_municipales()
    departamentos = servicio_departamento.obtener_departamentos()

    # Get selected department from request
    departamento_seleccionado = request.GET.get("departamento", "")

    # Filter reports by department
    if departamento_seleccionado:
        reportes_filtrados = [
            reporte for reporte in todos_reportes
            if reporte.obtener_departamento().nombre.lower() == departamento_seleccionado.lower()
        ]
    else:
        reportes_filtrados = todos_reportes

    return render(request, "entidad/reportes/lista_reportes.html", {
        "reportes": reportes_filtrados,
        "departamentos": departamentos,
        "departamento_seleccionado": departamento_seleccionado
    })
