import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.core.models import User
from crum import get_current_user
from datetime import datetime


# Create your models here.

class Estado(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre_corto = models.CharField(unique=True, max_length=2)
    nombre_completo = models.CharField(unique=True, max_length=50)

class ModeloBase(models.Model):
    fecha_crea = models.DateTimeField(auto_now_add=True, null=True)
    usuario_crea = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_creado', null=True, )
    fecha_modif = models.DateTimeField(auto_now=True, null=True)
    usuario_modif = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_modificado', null=True)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT, related_name='%(class)s_estado', null=True, default = 1)

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        self.usuario_modif = current_user 
        if self.pk == None :
            self.usuario_crea = current_user
        #super().save(*args, **kwargs)
        super(ModeloBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Pais(ModeloBase):
    nombre_corto = models.CharField(unique=True, max_length=2)
    nombre_completo = models.CharField(unique=True, max_length=50)
    icono = models.ImageField(upload_to ='uploads/maestros/paises/iconos/')

    def __str__(self):
        return self.nombre_completo

class Region(ModeloBase):
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name="region_pais")
    nombre_completo = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.nombre_completo


class Provincia(ModeloBase):
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="provincia_region")
    nombre_completo = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.nombre_completo

class Distrito(ModeloBase):
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, related_name="distrito_provincia")
    nombre_completo = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.nombre_completo

class TipoPersona(ModeloBase):
    nombre = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.nombre

class TipoSociedad(ModeloBase):
    nombre = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.nombre

class RedSocial(ModeloBase):
    nombre = models.CharField(max_length=50)
    icono = models.ImageField(upload_to ='uploads/maestros/redsocial/iconos/')
    orden = models.IntegerField()

    def __str__(self):
        return self.nombre

class Empresa(ModeloBase):
    numero_documento = models.CharField(unique=True, max_length=25)        
    razon_social = models.CharField(unique=True, max_length=250)        
    nombre_comercial = models.CharField(unique=True, max_length=250)        
    tipo_persona = models.ForeignKey(TipoPersona, on_delete=models.PROTECT, related_name="e_tipopersona")
    tipo_sociedad = models.ForeignKey(TipoSociedad, on_delete=models.PROTECT, related_name="e_tiposociedad")
    cantidad_trabajadores = models.IntegerField(default=0)

    def __str__(self):
        return self.razon_social

class PerfilUsuario(ModeloBase):
    nombre = models.CharField(unique=True, max_length=250)

class EmpresaUsuario(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="eu_empresa")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, related_name="eu_usuario")
    perfil = models.ForeignKey(PerfilUsuario, on_delete=models.PROTECT, related_name="eu_perfil")

class EmpresaArchivoTipo(ModeloBase):
    nombre = models.CharField(unique=True, max_length=50)

class EmpresaArchivo(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="ea_empresa")
    empresa_archivo_tipo = models.ForeignKey(EmpresaArchivoTipo, on_delete=models.PROTECT, related_name="ea_empresaarchivotipo")
    archivo = models.FileField(upload_to ='uploads/empresa/principal/documentos/')
    observaciones = models.TextField()

class EmpresaRedSocial(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="ers_empresa")
    red_social = models.ForeignKey(RedSocial, on_delete=models.PROTECT, related_name="ers_redsocial")
    url = models.CharField(max_length=250)

class EmpresaLocacionTipo(ModeloBase):
    nombre = models.CharField(unique=True,max_length=100)

    def __str__(self):
        return self.nombre

    # Oficina Administrativa
    # Produccion    

class EmpresaLocacion(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="el_empresa")
    empresa_locacion_tipo = models.ForeignKey(EmpresaLocacionTipo, on_delete=models.PROTECT, related_name="el_empresalocaciontipo")
    direccion = models.TextField()
    telefonos = models.CharField(max_length=25)
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name="el_pais")
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="el_region")
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, related_name="el_provincia")
    distrito = models.ForeignKey(Distrito, on_delete=models.PROTECT, related_name="el_distrito")
    latitud = models.DecimalField(max_digits=20, decimal_places=15)
    longitud = models.DecimalField(max_digits=20, decimal_places=15)
    foto = models.ImageField(upload_to ='uploads/empresa/locacion/foto/')

class EmpresaLocacionFotoTicket(ModeloBase):
    empresa_locacion = models.ForeignKey(EmpresaLocacion, on_delete=models.PROTECT, related_name="elft_empresalocacion")
    envio_id = models.UUIDField(default=uuid.uuid4, editable=False)
    fecha = models.DateTimeField(auto_now=True)
    usado = models.BooleanField(default=False)

class EmpresaRepresentanteTipo(ModeloBase):
    nombre = models.CharField(unique=True, max_length=250)
    
    def __str__(self):
        return self.nombre

class DocumentoIdentidadTipo(ModeloBase):
    nombre_corto = models.CharField(unique=True, max_length=10)
    nombre_completo = models.CharField(unique=True, max_length=250) 

    def __str__(self):
        return self.nombre_corto

class EmpresaRepresentante(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="emore_empresa")
    empresa_representante_tipo = models.ForeignKey(EmpresaRepresentanteTipo, on_delete=models.PROTECT, related_name="er_empresarepresentantetipo")
    documento_identidad_tipo = models.ForeignKey(DocumentoIdentidadTipo, on_delete=models.PROTECT, related_name="er_documentoidentidadtipo")
    numero_documento_identidad = models.CharField(max_length=15)
    pdf_documento_identidad = models.FileField(upload_to ='uploads/empresa/representantes/documentos/')
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField( max_length=100)
    nombres = models.CharField(max_length=100)
    correo = models.EmailField(max_length=100)
    nacionalidad = models.ForeignKey(Pais, on_delete=models.PROTECT, related_name="er_nacionalidad")
    telefonos = models.CharField(max_length=25)  

    def nombre_completo(self):
        return self.apellido_paterno + " " + self.apellido_materno + ", " + self.nombres 

    def apellidos(self):
        return self.apellido_paterno + " " + self.apellido_materno 

class Rubro(ModeloBase):
    nombre = models.CharField(max_length=250)

    def __str__(self):
        return self.nombre

class EmpresaRubro(ModeloBase):    
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="erubro_empresa")
    rubro = models.ForeignKey(Rubro, on_delete=models.PROTECT, related_name="erubro_rubro")
    etiquetas = models.JSONField(default=dict)

class ActividadEconomica(ModeloBase):
    codigo_ciiu = models.CharField(unique=True, max_length=25)
    nombre = models.CharField(max_length=250)

    def __str__(self):
        return self.codigo_ciiu + " - " +  self.nombre

class EmpresaActividadEconomica(ModeloBase):    
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="eac_empresa")
    orden = models.IntegerField()
    actividad_economica = models.ForeignKey(ActividadEconomica, on_delete=models.PROTECT, related_name="eac_actividadeconomica")

class Financiera(ModeloBase):
    nombre = models.TextField() 

class TipoCuentaBancaria(ModeloBase):
    nombre = models.CharField(unique=True,max_length=50)

class Moneda(ModeloBase):
    nombre = models.CharField(unique=True,max_length=25)
    nombre_corto = models.CharField(unique=True,max_length=5)

    def __str__(self):
        return self.nombre

class EmpresaInformacionBancaria(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="eib_empresa")
    financiera = models.ForeignKey(Financiera, on_delete=models.PROTECT, related_name="eib_financiera")
    tipo_cuenta = models.ForeignKey(TipoCuentaBancaria, on_delete=models.PROTECT, related_name="eib_tipocuenta")
    moneda_cuenta = models.ForeignKey(Moneda, on_delete=models.PROTECT, related_name="eib_monedacuenta")
    numero_cuenta = models.CharField(max_length=50)
    nombre_titular = models.CharField(max_length=100)
    certificado = models.FileField(upload_to ='uploads/empresa/infobancaria/certificados/')

class RegimenRecaudacion(ModeloBase):
    nombre = models.CharField(unique=True,max_length=50)

class InformacionTributaria(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="inftrib_empresa")
    regimen_recaudacion = models.ForeignKey(RegimenRecaudacion, on_delete=models.PROTECT, related_name="it_regimenrecaudacion")
    certificado = models.FileField(upload_to ='uploads/empresa/infotributaria/certificados/')

class EmpresaParticipacionAccionaria(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="emppartacc_empresa")
    empresa_representante = models.ForeignKey(EmpresaRepresentante, on_delete=models.PROTECT, related_name="emppartacc_empresarepresentante")
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)

class EmpresaExperiencia(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="empexp_empresa")
    cliente = models.CharField(max_length=100)
    fecha = models.DateField()
    moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, related_name="empexp_moneda")
    valor = models.DecimalField(max_digits=16, decimal_places=2)
    detalle = models.CharField(max_length=250)
    contacto_nombre = models.CharField(max_length=100)
    contacto_correo = models.CharField(max_length=100)
    contacto_telefono = models.CharField(max_length=20)

class EmpresaExperienciaDocumentacion(ModeloBase):
    empresa_experiencia = models.ForeignKey(EmpresaExperiencia, on_delete=models.PROTECT, related_name="expexpdoc_empresaexperiencia")
    descripcion = models.CharField(max_length=250)
    documento = models.FileField(upload_to ='uploads/empresa/experiencia/documentos/')

class Certificacion(ModeloBase):
    nombre = models.CharField(max_length=50)
    descricion = models.TextField()    
    
    def __str__(self):
        return self.nombre

class EmpresaCertificacion(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="empcert_empresa")
    certificacion = models.ForeignKey(Certificacion, on_delete=models.PROTECT, related_name="ec_certificacion")
    vigencia_desde = models.DateField()
    vigencia_hasta = models.DateField()
    proceso = models.CharField(max_length=100)
    comentarios = models.TextField()
    documento = models.FileField(upload_to ='uploads/empresa/certificaciones/documentos/')

class DocumentacionTipo(ModeloBase):
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre

class EmpresaDocumentacion(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="empdoc_empresa")
    documentacion_tipo = models.ForeignKey(DocumentacionTipo, on_delete=models.PROTECT, related_name="empdoc_documentaciontipo")
    descripcion = models.TextField()
    archivo = models.FileField(upload_to ='uploads/empresa/documentacion/documentos/')

class Tags(ModeloBase):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class EmpresaTags(ModeloBase):
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="et_empresa")
    #tags = models.ForeignKey(Tags, on_delete=models.PROTECT, related_name="et_tags")
    tags = models.JSONField(default=dict)
                 
# class EmpresaExperiencia(ModeloBase):
#     empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="ee_empresa")
#     cliente = models.CharField(max_length=100)
#     fecha = models.DateField()
#     detalle = models.TextField()
#     contacto_nombre = models.CharField(max_length=100)
#     contacto_correo = models.CharField(max_length=100)
#     contacto_telefono = models.CharField(max_length=9)

# class EmpresaInformacionFinanciera(ModeloBase):
#     empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT, related_name="eif_empresa")
#     periodo = models.IntegerField()
#     moneda = models.ForeignKey(Moneda, on_delete=models.PROTECT, related_name="eif_monedacuenta")
#     activo_corriente = models.DecimalField(16,2)
#     inventario = models.DecimalField(16,2)
#     activo_total = models.DecimalField(16,2)
#     pasivo_corriente = models.DecimalField(16,2)
#     obligaciones_financieras = models.DecimalField(16,2)
#     pasivo_total = models.DecimalField(16,2)
#     patrimonio = models.DecimalField(16,2)
#     utilidades_retenidas = models.DecimalField(16,2)
#     ventas_operacionales = models.DecimalField(16,2)
#     utilidades_operacionales = models.DecimalField(16,2)
#     utilidad_neta = models.DecimalField(16,2)
#     depreciacion_amortizacion = models.DecimalField(16,2)
#     gastos_financieros = models.DecimalField(16,2)
#     documento = models.FileField(upload_to ='uploads/empresa/infofinanciera/documentos/')

