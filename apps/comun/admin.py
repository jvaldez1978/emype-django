from django.contrib import admin
from .models import Empresa, Pais, Region, Provincia, Distrito, TipoPersona, TipoSociedad, PerfilUsuario,EmpresaRepresentanteTipo,DocumentoIdentidadTipo,EmpresaLocacionTipo,RedSocial,Certificacion, Moneda, EmpresaExperienciaDocumentacion, Rubro, EmpresaTags, Tags, EmpresaLocacion,DocumentacionTipo

@admin.register(Empresa, Pais, Region, Provincia, Distrito, TipoPersona, TipoSociedad, PerfilUsuario,EmpresaRepresentanteTipo,DocumentoIdentidadTipo,EmpresaLocacionTipo,RedSocial,Certificacion, Moneda, EmpresaExperienciaDocumentacion,Rubro, EmpresaTags, Tags,EmpresaLocacion,DocumentacionTipo )
class GeneralAdmin(admin.ModelAdmin):
    pass
