import requests
from math import radians, cos, sin, sqrt, atan2
from django.conf import settings
from shared.models.ciudad.sector import Sector

GOOGLE_MAPS_API_KEY = settings.GOOGLE_MAPS_API_KEY

def obtener_coordenadas(direccion):
    """
    Convierte una dirección en coordenadas (latitud y longitud) usando Google Maps API.
    """
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={direccion}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None

def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos geográficos usando la fórmula de Haversine.
    """
    R = 6371  # Radio de la Tierra en km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # Distancia en kilómetros

def obtener_sector_por_direccion(direccion):
    """
    Encuentra el sector más cercano a la dirección dada.
    """
    coordenadas = obtener_coordenadas(direccion)
    if not coordenadas:
        return None

    lat, lon = coordenadas
    sectores = Sector.objects.all()

    sector_mas_cercano = None
    distancia_minima = float("inf")

    for sector in sectores:
        distancia = calcular_distancia(lat, lon, sector.latitud, sector.longitud)
        if distancia <= sector.radio_km and distancia < distancia_minima:
            sector_mas_cercano = sector
            distancia_minima = distancia

    return sector_mas_cercano
