from django.db import models
from django.utils.translation import gettext_lazy as _

# Lista de sectores disponibles
SECTORES = [
    ('BELISARIO QUEVEDO', 'Belisario Quevedo'),
    ('EL INCA', 'El Inca'),
    ('CARCELÉN', 'Carcelén'),
    ('CENTRO HISTÓRICO', 'Centro Histórico'),
    ('CHILIBULO', 'Chilibulo'),
    ('CHILLOGALLO', 'Chillogallo'),
    ('CHIMBACALLE', 'Chimbacalle'),
    ('COCHAPAMBA', 'Cochapamba'),
    ('COMITÉ DEL PUEBLO', 'Comité del Pueblo'),
    ('CONCEPCIÓN', 'Concepción'),
    ('COTOCOLLAO', 'Cotocollao'),
    ('EL CONDADO', 'El Condado'),
    ('MAGDALENA', 'Magdalena'),
    ('GUAMANÍ', 'Guamaní'),
    ('IÑAQUITO', 'Iñaquito'),
    ('ITCHIMBÍA', 'Itchimbía'),
    ('JIPIJAPA', 'Jipijapa'),
    ('KENNEDY', 'Kennedy'),
    ('LA ARGELIA', 'La Argelia'),
    ('LA ECUATORIANA', 'La Ecuatoriana'),
    ('LA FERROVIARIA', 'La Ferroviaria'),
    ('LA LIBERTAD', 'La Libertad'),
    ('LA MENA', 'La Mena'),
    ('MARISCAL SUCRE', 'Mariscal Sucre'),
    ('PONCEANO', 'Ponceano'),
    ('PUENGASÍ', 'Puengasí'),
    ('QUITUMBE', 'Quitumbe'),
    ('RUMIPAMBA', 'Rumipamba'),
    ('SAN BARTOLO', 'San Bartolo'),
    ('SAN JUAN', 'San Juan'),
    ('SOLANDA', 'Solanda'),
    ('TURUBAMBA', 'Turubamba'),
]

# Definición de los estados posibles del sector
ESTADOS_SECTOR = [
    ('Seguro', 'Seguro'),
    ('En Riesgo', 'En Riesgo'),
    ('Peligroso', 'Peligroso'),
]

class Sector(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    estado = models.CharField(
        max_length=20,
        choices=[
            ('Seguro', 'Seguro'),
            ('Riesgo', 'Riesgo'),
            ('Peligroso', 'Peligroso')
        ],
        default='Seguro'
    )

    def _str_(self):
        return self.nombre  # Simplificado para evitar confusión