# Created by ASUS at 24/1/2025
# language: es
Característica: Notificar reportes de alta prioridad o el estado de un sector de interés
  Como ciudadano,
  Quiero recibir notificaciones de reportes de alta prioridad asociados a un incidente o el estado de un sector de mi interés
  Para poder tomar decisiones informadas y evitar situaciones de riesgo

  Escenario: Seleccionar sector de interés
    Dado que existen sectores en la ciudad y son
      | nombre_sector |
      | La Floresta   |
      | Chillogallo   |
      | La Magdalena  |
      | Solanda       |
      | La Mariscal   |
    Cuando el ciudadano "Andrés Cantuña" seleccione "Chillogallo" como sector de interés
    Entonces se agregará a la lista de sectores de interés

  Escenario: Notificar un reporte de alta prioridad en un sector de interés
    Dado que el ciudadano "Andrés Cantuña" tiene registrado "Solanda" como sector de interés
    Cuando se registre un reporte con asunto "Accidente"
    Y el estado del reporte no es "Resuelto"
    Entonces se enviará un correo con los detalles del reporte
    Y se agregará a la lista de notificaciones


  Escenario: Notificar cuando el estado de un sector de interés sea de riesgo
    Dado que el ciudadano "Andrés Cantuña" tiene registrado "Solanda" como sector de interés
    Cuando se registren al menos "5" reportes con asunto "Robo"
    Entonces el sector cambiará a estado "Riesgo"
    Y se enviará un correo con el mensaje "Precaución: el sector Solanda ha sido catalogado como de riesgo."
    Y se agregará a la lista de notificaciones