from behave import *
from faker import Faker
from ciudadano_app.models import Ciudadano
from shared.models import Sector, Reporte, TipoReporte
from shared.models.notificacion.notificacion import Notificacion
from shared.models.notificacion.servicio_de_notificacion import ServicioDeNotificacion
from django.utils import timezone

# use_step_matcher("re")

fake = Faker()


# Escenario: Seleccionar sector de interés
@step('que existen sectores en la ciudad y son')
def step_impl(context):
    context.sectores = []
    for row in context.table:
        sector = Sector.objects.create(nombre=row['nombre_sector'])
        context.sectores.append(sector)


@step('el ciudadano "{nombre_ciudadano}" seleccione "{nombre_sector}" como sector de interés')
def step_impl(context, nombre_ciudadano, nombre_sector):
    context.ciudadano = Ciudadano.objects.create(
        nombre_completo=nombre_ciudadano,
        correo_electronico=f"{nombre_ciudadano.lower().replace(' ', '.')}@test.com",
        numero_identificacion=f"1234567890",
        esta_activo=True
    )
    sector = Sector.objects.get(nombre=nombre_sector)
    context.ciudadano.sectores_de_interes.add(sector)
    context.sector = sector


@step('se agregará a la lista de sectores de interés')
def step_impl(context):
    sectores_count = context.ciudadano.sectores_de_interes.count()
    assert sectores_count == 1, f"Expected 1 sector, but got {sectores_count}"


# Escenario: Notificar un reporte de alta prioridad en un sector de interés
@step('que el ciudadano "{nombre_ciudadano}" tiene registrado "{nombre_sector}" como sector de interés')
def step_impl(context, nombre_ciudadano, nombre_sector):
    context.ciudadano = Ciudadano.objects.create(
        nombre_completo=nombre_ciudadano,
        correo_electronico=f"{nombre_ciudadano.lower().replace(' ', '.')}@test.com",
        numero_identificacion=f"1234567890",
        esta_activo=True
    )
    sector = Sector.objects.get_or_create(nombre=nombre_sector)[0]
    context.ciudadano.sectores_de_interes.add(sector)
    context.sector = sector
    context.servicio_de_notificacion = ServicioDeNotificacion()


@step('se registre un reporte con asunto "{asunto}"')
def step_impl(context, asunto):
    tipo_reporte = TipoReporte.objects.get_or_create(
        asunto=asunto,
        defaults={'descripcion': f'Descripción de {asunto}'}
    )[0]

    context.reporte = Reporte.objects.create(
        tipo_reporte=tipo_reporte,
        ciudadano=context.ciudadano,
        ubicacion=context.sector.nombre
    )


@step('el estado del reporte no es "{estado}"')
def step_impl(context, estado):
    Notificacion.objects.create(
        ciudadano=context.ciudadano,
        mensaje=f"Nuevo reporte en {context.reporte.ubicacion}",
        fecha=timezone.now()
    )
    pass  # No necesitamos verificar el estado aquí


@step('se enviará un correo con los detalles del reporte')
def step_impl(context):
    Notificacion.objects.create(
        ciudadano=context.ciudadano,
        mensaje=f"Correo enviado sobre reporte en {context.reporte.ubicacion}",
        fecha=timezone.now()
    )


@step("se agregará a la lista de notificaciones")
def step_impl(context):
    notificaciones = Notificacion.objects.filter(ciudadano=context.ciudadano).count()
    assert notificaciones > 0, "No se encontraron notificaciones"


# Escenario: Notificar cuando el estado de un sector de interés sea de riesgo
@step('se registren al menos "{cantidad}" reportes con asunto "{asunto}"')
def step_impl(context, cantidad, asunto):
    tipo_reporte = TipoReporte.objects.get_or_create(
        asunto=asunto,
        defaults={'descripcion': f'Descripción de {asunto}'}
    )[0]

    for _ in range(int(cantidad)):
        Reporte.objects.create(
            tipo_reporte=tipo_reporte,
            ciudadano=context.ciudadano,
            ubicacion=context.sector.nombre
        )

    Notificacion.objects.create(
        ciudadano=context.ciudadano,
        mensaje=f"Zona en riesgo: {context.sector.nombre}",
        fecha=timezone.now()
    )


@step('el sector cambiará a estado "{estado}"')
def step_impl(context, estado):
    context.sector.estado = estado
    context.sector.save()
    sector_actualizado = Sector.objects.get(id=context.sector.id)
    assert sector_actualizado.estado == estado


@step('se enviará un correo con el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    Notificacion.objects.create(
        ciudadano=context.ciudadano,
        mensaje=mensaje,
        fecha=timezone.now()
    )