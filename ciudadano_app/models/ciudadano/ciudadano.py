"""
Modelo principal de Ciudadano.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from ciudadano_app.models.ciudadano.gestor_ciudadano import GestorCiudadano
from django.utils.translation import gettext_lazy as _

class Ciudadano(AbstractBaseUser):
    """
    Modelo que representa a un ciudadano en el sistema municipal.
    Extiende el modelo base de usuario de Django para incluir campos específicos.
    """

    correo_electronico: models.EmailField = models.EmailField(
        unique=True,
        verbose_name="Correo Electrónico",
        help_text="Dirección de correo electrónico del ciudadano",
    )

    nombre_completo: models.CharField = models.CharField(
        max_length=120,
        verbose_name="Nombre Completo",
        help_text="Nombre completo del ciudadano",
    )

    numero_identificacion: models.CharField = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de Identificación",
        help_text="Número de documento de identidad del ciudadano",
    )

    esta_activo: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="¿Está Activo?",
        help_text="Indica si el ciudadano puede acceder al sistema",
    )

    es_staff: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name="¿Es Personal Administrativo?",
        help_text="Indica si el ciudadano puede acceder al panel de administración",
    )

    fecha_registro: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro",
        help_text="Fecha y hora en que el ciudadano se registró en el sistema",
    )

    is_active: models.BooleanField = models.BooleanField(default=True)
    is_admin: models.BooleanField = models.BooleanField(default=False)

    sectores_de_interes = models.ManyToManyField(
        'shared.Sector',
        related_name="ciudadanos_interesados",
        blank=True
    )

    ubicacion_actual = models.ForeignKey(
        'shared.Sector',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ciudadanos_presentes"
    )

    sector = models.ForeignKey(
        'shared.Sector',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Sector")
    )

    objects = GestorCiudadano()

    USERNAME_FIELD = "correo_electronico"
    EMAIL_FIELD = "correo_electronico"
    REQUIRED_FIELDS = ["nombre_completo", "numero_identificacion"]

    def obtener_nombre_completo(self):
        """Retorna el nombre completo del ciudadano"""
        return self.nombre_completo

    def clean(self):
        super().clean()
        if EntidadMunicipal.objects.filter(correo_electronico=self.correo_electronico).exists():
            raise ValidationError({
                'correo_electronico': "Este correo ya está registrado como Entidad Municipal."
            })

    def obtener_correo_electronico(self):
        """Retorna el correo electrónico del ciudadano"""
        return self.correo_electronico

    def obtener_identificacion(self):
        """Retorna el número de identificación del ciudadano"""
        return self.numero_identificacion

    def agregar_sector_de_interes(self, sector):
        """Agrega un sector a la lista de sectores de interés del ciudadano."""
        self.sectores_de_interes.add(sector)
        self.save()

    def actualizar_ubicacion(self, sector):
        """Actualiza la ubicación actual del ciudadano."""
        self.ubicacion_actual = sector
        self.save()

    def _str_(self):
        """Retorna una representación en cadena del ciudadano"""
        return f"Ciudadano: {self.nombre_completo} ({self.correo_electronico})"
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def es_ciudadano(self):
        """Identifica que este usuario es un ciudadano"""
        return True

    class Meta:
        verbose_name = "Ciudadano"
        verbose_name_plural = "Ciudadanos"
        ordering = ["-fecha_registro"]