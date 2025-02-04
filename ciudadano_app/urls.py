from django.urls import path
from . import views
from .views.canales.noticia import reaccionar, comentar, conteo_reacciones
from .views.canales.suscripcion import suscribirse_canal, desuscribirse_canal
from .views.canales.notificacion import listar_notificacion
from .views.canales.canales import lista_canales, detalle_canal, ver_noticias
from shared.views.logout import logout_usuario
from .views.eventos.lista_eventos import (
    lista_eventos, 
    inscribirse_evento, 
    cancelar_inscripcion, 
    lista_espera_evento
)

urlpatterns = [
    path('canal/<int:canal_id>/suscribirse/', suscribirse_canal, name='suscribirse_canal'),
    path('canal/<int:canal_id>/desuscribirse/', desuscribirse_canal, name='desuscribirse_canal'),
    path('canal/<int:canal_id>/detalle/', detalle_canal, name='detalle_canal'),
    path('canal/lista_canales/', lista_canales, name='lista_canales'),
    path('muro/', ver_noticias, name='ver_noticias'),
    path('notificaciones/', listar_notificacion, name='ver_notificaciones'),
    path('muro/reaccion/<int:noticia_id>', reaccionar, name='reaccionar'),
    path('muro/conteo/<int:noticia_id>/', conteo_reacciones, name='conteo_reacciones'),
    path('muro/comentario/<int:noticia_id>/', comentar, name='comentar'),
    # URLs para autenticación de ciudadano
    path('', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('dashboard/', views.dashboard_ciudadano, name='dashboard_ciudadano'),
    path('bienvenida/', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('login/', views.login_ciudadano, name='login_ciudadano'),
    path('logout/', logout_usuario, name='logout_ciudadano'),
    path('eventos/', lista_eventos, name='lista_eventos'),
    path('eventos/<int:evento_id>/inscribirse/', inscribirse_evento, name='inscribirse_evento'),
    path('eventos/<int:evento_id>/cancelar/', cancelar_inscripcion, name='cancelar_inscripcion'),
    path('eventos/<int:evento_id>/lista-espera/', lista_espera_evento, name='lista_espera_evento'),
    path('reporte/', views.envio_reporte, name='envio_reporte'),
]
