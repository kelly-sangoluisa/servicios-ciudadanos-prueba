from .reporte import Reporte
from .repositorio_de_reporte import RepositorioDeReporte


class ServicioDeReporte():
    def __init__(self, reporte_repositorio: RepositorioDeReporte):
        """
        Inicializa el ServicioDeReporte con un repositorio de reportes.

        Args:
            reporte_repositorio (RepositorioDeReporte): Un objeto repositorio que implementa la interfaz
            para operaciones CRUD sobre reportes.
        """
        self.reporte_repositorio = reporte_repositorio

    def __obtener_prioridad(self, cantidad_reportes):
        """
        Determina la prioridad del reporte según la cantidad de reportes previos similares,
        utilizando la escala de Fibonacci: 1, 1, 2, 3, 5, 8, 13.

        Args:
            cantidad_reportes (int): Número de reportes previos con el mismo asunto.

        Returns:
            int: Nivel de prioridad asignado al reporte.
        """
        if cantidad_reportes >= 13:
            return 1
        if cantidad_reportes >= 8:
            return 2
        if cantidad_reportes >= 5:
            return 3
        if cantidad_reportes >= 3:
            return 4
        if cantidad_reportes >= 0:
            return 5

    def priorizar(self, reporte: Reporte):
        """
        Asigna una prioridad a un reporte basado en la cantidad de reportes previos con el mismo asunto.

        Args:
            reporte (Reporte): El reporte a priorizar.

        Returns:
            Reporte: El reporte con su prioridad actualizada.
        """
        reportes_previos = self.reporte_repositorio.obtener_reportes_por_asunto(reporte.tipo_reporte.asunto) or []
        cantidad_reportes = len(reportes_previos)
        reporte.prioridad = self.__obtener_prioridad(cantidad_reportes)
        self.reporte_repositorio.actualizar_prioridad_de_reporte_por_asunto(reporte.tipo_reporte.asunto,
                                                                            reporte.prioridad)
        return reporte

    def enviar_reporte(self, reporte: Reporte):
        """
        Valida y envía un reporte al repositorio para ser agregado a la base de datos.

        Args:
            reporte (Reporte): El reporte a enviar.

        Raises:
            ValueError: Si el reporte no es válido.
        """
        if not reporte.validar_reporte():
            raise ValueError("El reporte no es válido.")
        self.reporte_repositorio.agregar_reporte(reporte)
        
        return reporte
