from django.shortcuts import render
from ...decorators import ciudadano_required
from shared.models import ServicioDeReporte, RepositorioDeReporteDjango, Reporte
from shared.models.reporte.tipo_reporte import TipoReporte

repositorioReporte = RepositorioDeReporteDjango()
servicioDeReporte = ServicioDeReporte(repositorioReporte)

@ciudadano_required
def envio_reporte(request):
    """Envio de reportes"""
    if request.method == 'POST':
        ciudadano = request.user
        asunto = request.POST.get('asunto')
        ubicacion = request.POST.get('ubicacion')
        
        reporte = Reporte(
            ciudadano=ciudadano,
            tipo_reporte=TipoReporte.objects.get(asunto=asunto),
            ubicacion=ubicacion
        )
        
        reporte = servicioDeReporte.enviar_reporte(reporte=reporte)
        servicioDeReporte.priorizar(reporte)
        return render(request, 'reporte/envio_reporte.html', {'tipo_reportes': TipoReporte.objects.all(), 'success_message': 'Report sent successfully'})
    else:
        tipo_reportes = TipoReporte.objects.all()
        return render(request, 'reporte/envio_reporte.html', {'tipo_reportes': tipo_reportes})