from django.db import models
from shared.models.ciudad.sector import Sector
from django.shortcuts import get_object_or_404

# Lista de sectores predeterminados
SECTORES = [
    {"nombre": "Belisario Quevedo", "latitud": -0.2100, "longitud": -78.5000},
    {"nombre": "El Inca", "latitud": -0.1500, "longitud": -78.4700},
    {"nombre": "Carcelén", "latitud": -0.0800, "longitud": -78.4800},
    {"nombre": "Centro Histórico", "latitud": -0.2200, "longitud": -78.5100},
    {"nombre": "Chilibulo", "latitud": -0.2700, "longitud": -78.5700},
    {"nombre": "Chillogallo", "latitud": -0.3000, "longitud": -78.5500},
    {"nombre": "Chimbacalle", "latitud": -0.2500, "longitud": -78.5200},
    {"nombre": "Cochapamba", "latitud": -0.1800, "longitud": -78.4900},
    {"nombre": "Comité del Pueblo", "latitud": -0.1200, "longitud": -78.4600},
    {"nombre": "Concepción", "latitud": -0.1600, "longitud": -78.4800},
    {"nombre": "Cotocollao", "latitud": -0.1000, "longitud": -78.4900},
    {"nombre": "El Condado", "latitud": -0.0900, "longitud": -78.5000},
    {"nombre": "Magdalena", "latitud": -0.2600, "longitud": -78.5300},
    {"nombre": "Guamaní", "latitud": -0.3300, "longitud": -78.5500},
    {"nombre": "Iñaquito", "latitud": -0.1900, "longitud": -78.4900},
    {"nombre": "Itchimbía", "latitud": -0.2200, "longitud": -78.5000},
    {"nombre": "Jipijapa", "latitud": -0.1700, "longitud": -78.4800},
    {"nombre": "Kennedy", "latitud": -0.1400, "longitud": -78.4700},
    {"nombre": "La Argelia", "latitud": -0.2800, "longitud": -78.5200},
    {"nombre": "La Ecuatoriana", "latitud": -0.3200, "longitud": -78.5400},
    {"nombre": "La Ferroviaria", "latitud": -0.2700, "longitud": -78.5100},
    {"nombre": "La Libertad", "latitud": -0.2300, "longitud": -78.5200},
    {"nombre": "La Mena", "latitud": -0.2900, "longitud": -78.5400},
    {"nombre": "Mariscal Sucre", "latitud": -0.2100, "longitud": -78.4900},
    {"nombre": "Ponceano", "latitud": -0.0800, "longitud": -78.4700},
    {"nombre": "Puengasí", "latitud": -0.2500, "longitud": -78.5000},
    {"nombre": "Quitumbe", "latitud": -0.3100, "longitud": -78.5500},
    {"nombre": "Rumipamba", "latitud": -0.2000, "longitud": -78.5000},
    {"nombre": "San Bartolo", "latitud": -0.2700, "longitud": -78.5300},
    {"nombre": "San Juan", "latitud": -0.2200, "longitud": -78.5100},
    {"nombre": "Solanda", "latitud": -0.2900, "longitud": -78.5300},
    {"nombre": "Turubamba", "latitud": -0.3000, "longitud": -78.5400},
]

class Ciudad(models.Model):
    """
    Modelo que representa una ciudad y su relación con sectores.
    """

    # Atributos (Campos de la base de datos)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

    # Métodos
    def agregar_sectores(self, sectores):
        """
        Método para agregar sectores a la ciudad.
        """
        for sector_data in sectores:
            sector = Sector(
                nombre=sector_data["nombre"],
                latitud=sector_data["latitud"],
                longitud=sector_data["longitud"],
                ciudad=self
            )
            sector.save()

    @classmethod
    def crear_ciudad_con_sectores(cls, nombre_ciudad):
        """
        Método optimizado para crear una ciudad con sectores predeterminados.
        """
        ciudad, created = cls.objects.get_or_create(nombre=nombre_ciudad)
        if created:  # Solo creamos sectores si la ciudad fue creada
            sectores_a_crear = [
                Sector(
                    nombre=sector_data["nombre"],
                    latitud=sector_data["latitud"],
                    longitud=sector_data["longitud"],
                    ciudad=ciudad
                )
                for sector_data in SECTORES
            ]
            Sector.objects.bulk_create(sectores_a_crear)  # Inserta todos los sectores en una sola consulta
        return ciudad

    @classmethod
    def obtener_sectores_por_ciudad(cls, ciudad_id):
        """
        Método seguro para obtener los sectores de una ciudad dada.
        """
        ciudad = get_object_or_404(cls, id=ciudad_id)
        return ciudad.sectores.all()

    @classmethod
    def obtener_ciudades_con_sectores(cls):
        """
        Método para obtener todas las ciudades con sus sectores.
        """
        ciudades = cls.objects.all()
        ciudades_con_sectores = {}
        for ciudad in ciudades:
            sectores = ciudad.sectores.all()  # Aquí usamos el 'related_name' correcto
            ciudades_con_sectores[ciudad.nombre] = [sector.nombre for sector in sectores]
        return ciudades_con_sectores

