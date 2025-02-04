"""
URLs para la aplicación de entidad municipal.
"""
from django.urls import path
from . import views
from .views.canales import gestion_canal
from .views.canales import gestion_noticias
from shared.views.logout import logout_usuario
from .views.eventos.evento import actualizar_asistencia, eliminar_inscripcion

urlpatterns = [
    path('', views.bienvenida_entidad, name='bienvenida_entidad'),
    path('login/', views.login_entidad, name='login_entidad'),
    path('dashboard/', views.dashboard_entidad, name='dashboard_entidad'),
    path('lista_canales/', gestion_canal.listar_canales_administrados, name='listar_canales_administrados'),
    path('crear_canal/', gestion_canal.crear_canal, name='crear_canal'),
    path('crear_canal_form/', gestion_canal.crear_canal_form, name='crear_canal_form'),
    path('eliminar_canal/<int:canal_id>', gestion_canal.eliminar_canal, name='eliminar_canal'),
    path('lista_canales/noticias_canal/<int:canal_id>', gestion_noticias.noticias_canal, name='noticias_canal'),
    path('lista_canales/noticias_canal/crear_noticia/<int:canal_id>', gestion_noticias.crear_noticia, name='crear_noticia'),
    path('lista_canales/noticias_canal/detalle_noticia/<int:noticia_id>', gestion_noticias.detalle_noticia, name='detalle_noticia'),
    path('lista_canales/noticias_canal/detalle_noticia/eliminar_noticia/<int:noticia_id>', gestion_noticias.eliminar_noticia, name='eliminar_noticia'),
    path('lista_canales/noticias_canal/crear_alerta_emergencia/<int:canal_id>', gestion_noticias.alerta_de_emergencia, name='alerta_emergencia'),
    path('eventos/', views.gestor_eventos, name='gestor_eventos'),
    path('eventos/<int:evento_id>/', views.evento, name='detalle_evento'),
    path('eventos/asistencia/<int:registro_id>/', actualizar_asistencia, name='actualizar_asistencia'),
    path('eventos/inscripcion/<int:registro_id>/', eliminar_inscripcion, name='eliminar_inscripcion'),
    path('reportes/', views.lista_todos_reportes, name='lista_todos_reportes'),
    path('reportes/<int:reporte_id>/postergar/', views.postergar_reporte, name='postergar_reporte'),
    # path('reportes/<str:departamento>/', views.reportes_por_departamento, name='reportes_por_departamento'),
    path('reportes/<int:reporte_id>/resolver/', views.resolver_reporte, name='resolver_reporte'),
path('reporte/<int:reporte_id>/agregar_evidencia/', views.agregar_evidencia, name='agregar_evidencia'),

    path('eventos/<int:evento_id>/editar_evento/', views.editar_evento, name='editar_evento'),
    path('eventos/crear_evento/', views.crear_evento, name='crear_evento'),
    path('eventos/<int:evento_id>/actualizar_estado_incidente_evento/', views.actualizar_estado_incidente_evento, name='actualizar_estado_incidente_evento'),
    path('eventos/<int:evento_id>/cancelar_evento/', views.cancelar_evento, name='cancelar_evento'),
    path('eventos/espacios_disponibles/', views.espacios_publicos_disponibles, name='espacios_disponibles')


]
