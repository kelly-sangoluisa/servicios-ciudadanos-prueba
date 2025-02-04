from django.contrib import admin
from .models.reporte.tipo_reporte import TipoReporte
from .models.reporte.reporte import Reporte

@admin.register(TipoReporte)
class TipoReporteAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'descripcion', 'departamento', 'prioridad_de_atencion')
    search_fields = ('asunto', 'descripcion')

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin): 
    list_display = ('ciudadano', 'tipo_reporte', 'ubicacion', 'prioridad')