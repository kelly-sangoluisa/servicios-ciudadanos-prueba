from .dashboard import dashboard_ciudadano
from .registro import registro_ciudadano
from .login import login_ciudadano
from .bienvenida import bienvenida_ciudadano
from .eventos.lista_eventos import lista_eventos
from .reporte.envio_reporte import envio_reporte

__all__ = [
    'dashboard_ciudadano',
    'registro_ciudadano',
    'login_ciudadano',
    'bienvenida_ciudadano',
    'lista_eventos',
    'envio_reporte',
]