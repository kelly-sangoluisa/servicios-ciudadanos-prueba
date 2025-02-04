from threading import Lock

from faker import Faker
from entidad_municipal_app.models.reporte.repositorio_de_reporte_municipal import RepositorioDeReporteMunicipal
from entidad_municipal_app.models.reporte.reporte_municipal import ReporteMunicipal
from mocks.repositorio_de_departamento_en_memoria import RepositorioDeDepartamentoEnMemoria
from shared.models import TipoReporte, Reporte
from ciudadano_app.models import Ciudadano


class RepositorioDeReporteMunicipalEnMemoria(RepositorioDeReporteMunicipal):
    """
    Implementación de repositorio que almacena reportes municipales en memoria como Singleton.
    """

    _instance = None
    _lock = Lock()  # Thread safety for Singleton

    def __new__(cls, *args, **kwargs):
        """
        Implementación Singleton: Garantiza que solo haya una instancia del repositorio.
        """
        with cls._lock:  # Evita problemas de concurrencia
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.__initialized = False  # Flag para evitar re-inicialización
        return cls._instance

    def __init__(self):
        """
        Inicializa el repositorio con reportes de prueba generados con Faker (solo una vez).
        """
        if not self.__initialized:
            self.__initialized = True  # Marcar como inicializado
            self.reportes = {}
            self.next_id = 1
            self.fake = Faker('es_ES')
            self._generar_reportes_prueba()  # Generar datos de prueba

    def _generar_reportes_prueba(self):
        """
        Genera reportes municipales de prueba con datos ficticios.
        """
        estados_validos = ["no_asignado", "asignado", "atendiendo", "resuelto", "postergado"]
        repositorio_departamentos = RepositorioDeDepartamentoEnMemoria()
        nombres_departamentos = [
            "EPMMOP",  # Empresa Pública Metropolitana de Movilidad y Obras Públicas
            "Obras Públicas",
            "Seguridad Ciudadana",
            "Medio Ambiente",
            "Desarrollo Urbano",
            "Servicios Públicos",
            "Gestión de Riesgos"
        ]
        for _ in range(5):  # Generamos 5 reportes ficticios
            ciudadano = Ciudadano(
                nombre_completo=self.fake.name(),
                correo_electronico=self.fake.email(),
                numero_identificacion=self.fake.numerify(text="##########")
            )

            tipo_reporte = TipoReporte(
                asunto=self.fake.sentence(nb_words=4),
                descripcion=self.fake.text(max_nb_chars=200),
                departamento = repositorio_departamentos.obtener_departamento_por_nombre(self.fake.random_element(elements=nombres_departamentos)),
                prioridad_de_atencion = self.fake.random_int(min=1, max=3)
            )

            reporte_ciudadano = Reporte(
                ciudadano=ciudadano,
                tipo_reporte=tipo_reporte,
                ubicacion=self.fake.address(),
                prioridad=self.fake.random_int(min=1, max=5)
            )

            estado = "asignado"
            self.crear(reporte_ciudadano, estado)

    def obtener_por_id(self, id_reporte: int):
        """
        Obtiene un reporte por su ID.

        Args:
            id_reporte (int): ID del reporte municipal.

        Returns:
            ReporteMunicipal | None: Reporte si existe, None si no existe.
        """
        return self.reportes.get(id_reporte)

    def obtener_todos(self):
        """
        Obtiene todos los reportes almacenados en memoria.

        Returns:
            list[ReporteMunicipal]: Lista de reportes municipales.
        """
        return list(self.reportes.values())

    def obtener_por_estado(self, estado: str):
        """
        Obtiene reportes filtrados por estado.

        Args:
            estado (str): Estado del reporte municipal.

        Returns:
            list[ReporteMunicipal]: Lista de reportes con el estado indicado.
        """
        return [r for r in self.reportes.values() if r.estado == estado]

    def crear(self, reporte_ciudadano: Reporte, estado="no_asignado"):
        """
        Crea un nuevo reporte municipal.

        Args:
            reporte_ciudadano (Reporte): Reporte ciudadano original.
            estado (str, opcional): Estado inicial del reporte. Por defecto es 'no_asignado'.

        Returns:
            ReporteMunicipal: El reporte municipal creado.
        """
        reporte_municipal = ReporteMunicipal(
            id=self.next_id,
            reporte_ciudadano=reporte_ciudadano,
            estado=estado
        )
        self.reportes[self.next_id] = reporte_municipal
        self.next_id += 1
        return reporte_municipal

    def actualizar(self, reporte_municipal):
        """
        Actualiza un reporte existente.

        Args:
            reporte_municipal (ReporteMunicipal): Reporte municipal actualizado.

        Returns:
            ReporteMunicipal | None: Reporte actualizado o None si no existe.
        """
        if reporte_municipal.id in self.reportes:
            self.reportes[reporte_municipal.id] = reporte_municipal
            return reporte_municipal
        return None

    def eliminar(self, id_reporte: int):
        """
        Elimina un reporte municipal por su ID.

        Args:
            id_reporte (int): ID del reporte a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existía.
        """
        if id_reporte in self.reportes:
            del self.reportes[id_reporte]
            return True
        return False

