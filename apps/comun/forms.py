from django.forms import ModelForm
from .models import Empresa, EmpresaRepresentante, EmpresaLocacion, EmpresaRedSocial, EmpresaActividadEconomica, EmpresaCertificacion, EmpresaExperiencia, EmpresaExperienciaDocumentacion, EmpresaRubro, EmpresaCertificacion,EmpresaDocumentacion
from django import forms

class empForm(ModelForm):
    class Meta:
        model = Empresa
        fields = '__all__'

class empNuevaForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ('numero_documento','razon_social','nombre_comercial','tipo_persona','tipo_sociedad','cantidad_trabajadores')

class empEditarForm(ModelForm):
    class Meta:
        model = Empresa
        fields = ('razon_social','nombre_comercial','tipo_persona','tipo_sociedad','cantidad_trabajadores')


class empresaRepresentanteForm(ModelForm):
    class Meta:
        model = EmpresaRepresentante
        fields = ('empresa_representante_tipo','documento_identidad_tipo','documento_identidad_tipo','numero_documento_identidad','nacionalidad','apellido_paterno','apellido_materno','nombres','correo','telefonos')


class empresaLocacionForm(ModelForm):
    class Meta:
        model = EmpresaLocacion
        fields = ('empresa_locacion_tipo','direccion','telefonos','pais','region','provincia','distrito','latitud', 'longitud')

class empresaLocacionFotoForm(ModelForm):
    class Meta:
        model = EmpresaLocacion
        fields = ('empresa_locacion_tipo','direccion','telefonos','pais','region','provincia','distrito','latitud', 'longitud', 'foto')


class empresaRedSocialForm(ModelForm):
    class Meta:
        model = EmpresaRedSocial
        fields = ('red_social','url')

class empresaActividadEconomicaForm(ModelForm):
    class Meta:
        model = EmpresaActividadEconomica
        fields = ('actividad_economica','orden')

class empresaRubroForm(ModelForm):
    etiquetas = forms.CharField(widget= forms.Textarea)

    class Meta:
        model = EmpresaRubro
        fields = ('rubro','etiquetas')

class empresaDocumentacionForm(ModelForm):
    archivo = forms.FileField(required=False)

    class Meta:
        model = EmpresaDocumentacion
        fields = ('documentacion_tipo','descripcion','archivo')

class empresaCertificacionForm(ModelForm):
    class Meta:
        model = EmpresaCertificacion
        fields = ('certificacion','proceso','vigencia_desde','vigencia_hasta')

class empresaExperienciaForm(ModelForm):
    class Meta:
        model = EmpresaExperiencia
        fields = ('cliente','fecha','moneda','valor','detalle','contacto_nombre','contacto_correo','contacto_telefono')

class empresaExperienciaSustentoForm(ModelForm):
    class Meta:
        model = EmpresaExperienciaDocumentacion
        fields = ('descripcion','documento')

# class EmpresaExperiencia(models.Model):
#     empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="empexp_empresa")
#     cliente = models.CharField(max_length=100)
#     fecha = models.DateField()
#     moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, related_name="empexp_moneda")
#     valor = models.DecimalField(max_digits=16, decimal_places=2)
#     detalle = models.CharField(max_length=250)
#     contacto_nombre = models.CharField(max_length=100)
#     contacto_correo = models.CharField(max_length=100)
#     contacto_telefono = models.CharField(max_length=20)

class ImageUploadForm(forms.Form):
    """Image upload form."""
    foto = forms.ImageField()