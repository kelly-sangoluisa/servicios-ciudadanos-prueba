from django.shortcuts import render, redirect
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models import EntidadMunicipal
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo

def listar_canales_administrados(request):
    """
        Muestra una lista de los canales informativos administrados por la entidad municipal.

        Esta vista obtiene los canales informativos asociados a la entidad municipal que está logueada (basado en el usuario
        autenticado), y los pasa al template para su renderizado.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.

        Returns:
            HttpResponse: El renderizado del template 'canales/lista_canales_administrados.html', con la lista de canales.
    """
    entidad_municipal = EntidadMunicipal.objects.get(id = request.user.id)
    canales = CanalInformativo.objects.filter(entidad_municipal = entidad_municipal)
    return render(request, 'canales/lista_canales_administrados.html',{'canales':canales})

def crear_canal_form(request):
    """
        Muestra el formulario para crear un nuevo canal informativo.

        Esta vista solo renderiza el template que contiene el formulario de creación de un canal.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.

        Returns:
            HttpResponse: El renderizado del template 'canales/crear_canal.html', con el formulario para crear un canal.
    """
    return render(request, 'canales/crear_canal.html')

def crear_canal(request):
    """
        Crea un nuevo canal informativo y lo suscribe a todos los ciudadanos si es de emergencia.

        Esta vista maneja el formulario de creación de un canal. Al recibir una solicitud POST, crea un nuevo canal
        informativo basado en los datos enviados en el formulario. Si el canal es de emergencia, suscribe a todos los ciudadanos
        al canal recién creado.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario que contiene los datos del formulario.

        Returns:
            HttpResponseRedirect: Redirige a la lista de canales de la entidad municipal después de crear el canal.
    """
    if request.method == 'POST':
        entidad_municipal = EntidadMunicipal.objects.get(id=request.user.id)
        nombre = request.POST.get('nombre_canal')
        descripcion = request.POST.get('descripcion_canal')
        es_emergencia = request.POST.get('es_emergencia')
        if nombre and descripcion and es_emergencia:
            CanalInformativo.objects.create(
                entidad_municipal=entidad_municipal,
                nombre=nombre,
                descripcion=descripcion,
                es_emergencia=es_emergencia
            )
            canal = CanalInformativo.objects.get(nombre=nombre)
            if canal.es_emergencia:
                ciudadanos = Ciudadano.objects.all()
                for ciudadano in ciudadanos:
                    canal.suscribir_ciudadano(ciudadano)
    return redirect("/entidad_municipal/lista_canales/")

def eliminar_canal(request,canal_id):
    """
        Elimina un canal informativo de la base de datos.

        Esta vista recibe el identificador de un canal y lo elimina de la base de datos. Luego, redirige a la lista de canales
        administrados por la entidad municipal.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            canal_id (int): El identificador único del canal a eliminar.

        Returns:
            HttpResponseRedirect: Redirige a la lista de canales de la entidad municipal después de eliminar el canal.
    """
    canal= CanalInformativo.objects.get(id=canal_id)
    canal.delete()
    return redirect("/entidad_municipal/lista_canales/")