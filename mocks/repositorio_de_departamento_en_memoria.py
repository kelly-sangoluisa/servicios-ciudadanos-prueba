from threading import Lock

from faker import Faker
from entidad_municipal_app.models.departamento.departamento import Departamento
from entidad_municipal_app.models.departamento.repositorio_departamento import RepositorioDepartamento


class RepositorioDeDepartamentoEnMemoria(RepositorioDepartamento):
    """
    Implementación de un repositorio que almacena departamentos en memoria como Singleton.
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
        Inicializa el repositorio con algunos departamentos de prueba generados con Faker (solo una vez).
        """
        if not self.__initialized:
            self.__initialized = True  # Marcar como inicializado
            self.departamentos = {}
            self.fake = Faker('es_ES')
            self.next_id = 1  # Variable para asignar IDs únicos en memoria
            self._generar_departamentos_prueba()  # Generar datos de prueba

    def _generar_departamentos_prueba(self):
        """
        Genera departamentos de prueba con nombres realistas.
        """
        nombres_departamentos = [
            "EPMMOP",  # Empresa Pública Metropolitana de Movilidad y Obras Públicas
            "Obras Públicas",
            "Seguridad Ciudadana",
            "Medio Ambiente",
            "Desarrollo Urbano",
            "Servicios Públicos",
            "Gestión de Riesgos"
        ]

        for nombre in nombres_departamentos:
            descripcion = self.fake.sentence(nb_words=10)  # Genera una descripción aleatoria
            departamento = Departamento(nombre=nombre, descripcion=descripcion)  # Asigna un ID manualmente
            self.departamentos[nombre.upper()] = departamento
            self.next_id += 1  # Incrementa el ID para el siguiente departamento

    def obtener_departamento_por_nombre(self, nombre: str):
        """
        Obtiene un departamento por su nombre.

        Args:
            nombre (str): Nombre del departamento.

        Returns:
            Departamento: Instancia del departamento o None si no existe.
        """
        return self.departamentos.get(nombre.upper())

    def listar_departamentos(self):
        """
        Obtiene todos los departamentos almacenados en memoria.

        Returns:
            list[Departamento]: Lista de todos los departamentos en memoria.
        """
        return list(self.departamentos.values())

    def agregar_departamento(self, departamento: Departamento):
        """
        Agrega un nuevo departamento al repositorio.

        Args:
            departamento (Departamento): Instancia del departamento a agregar.
        """
        departamento.id = self.next_id  # Asigna un ID único
        self.departamentos[departamento.nombre.upper()] = departamento
        self.next_id += 1  # Incrementa el ID

    def actualizar_descripcion_departamento(self, nombre: str, nueva_descripcion: str):
        """
        Actualiza la descripción de un departamento.

        Args:
            nombre (str): Nombre del departamento a actualizar.
            nueva_descripcion (str): Nueva descripción del departamento.
        """
        nombre = nombre.upper()
        if nombre in self.departamentos:
            self.departamentos[nombre].descripcion = nueva_descripcion
            return True
        return False

    def eliminar_departamento(self, nombre: str):
        """
        Elimina un departamento por su nombre.

        Args:
            nombre (str): Nombre del departamento a eliminar.

        Returns:
            bool: True si se eliminó correctamente, False si no existía.
        """
        nombre = nombre.upper()
        if nombre in self.departamentos:
            del self.departamentos[nombre]
            return True
        return False
