from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
import uuid

urlpatterns = [
    path('ajax/getemp/', views.obtieneEmpresa, name='obtiene_empresa'),

    path('', views.empresaHome, name='home'),
    path('emphome/', views.empresaHome, name='empresa_home'),
    path('empadd/', views.empresaAdd, name='empresa_add'),
    path('empedit/', views.empresaEdit, name='empresa_edit'),
    path('empview/', views.empresaView, name='empresa_view'),

    path('emp/postajax/', views.postEmpresa, name = "empresa_postajax"),

#########################

    path('emprep/postajax/', views.postRepresentanteEmpresa, name = "empresa_rep_postajax"),
    path('emprep/postajaxdel/<int:id>', views.deleteRepresentanteEmpresa, name = "empresa_rep_postajax_del"),
    
    path('emprepadd/', views.empresaRepresentanteAdd, name='empresa_rep_add'),
    path('empreplist/', views.empresaRepresentanteList, name='empresa_rep_list'),
    path('emprepedit/<int:id>', views.empresaRepresentanteEdit, name='empresa_rep_edit'),
    path('emprepview/<int:id>', views.empresaRepresentanteView, name='empresa_rep_view'),

#########################

    path('emploc/postajax/', views.postEmpresaLocacion, name = "empresa_loc_postajax"),
    path('emploc/postajaxdel/<int:id>', views.deleteEmpresaLocacion, name = "empresa_loc_postajax_del"),
    path('emploc/postajaxfoto/<int:id>', views.postEmpresaLocacionFoto, name = "empresa_loc_postajax_foto"),
    #path('emploc/uploadfoto/<int:id>', views.postEmpresaLocacionFotoUpload, name = "empresa_loc_upload_foto"),

    path('fotoloc/<uuid:envio_id>', views.pruebafoto, name = "pruebafoto"),

    path('emplocadd/', views.empresaLocacionAdd, name='empresa_loc_add'),
    path('emploclist/', views.empresaLocacionList, name='empresa_loc_list'),
    path('emplocedit/<int:id>', views.empresaLocacionEdit, name='empresa_loc_edit'),
    path('emplocview/<int:id>', views.empresaLocacionView, name='empresa_loc_view'),
    path('emplocjson/<int:id>', views.LocacionJSONGet, name='empresa_loc_json'),

    path('empacteadd/', views.empresaActividadEconomicaAdd, name='empresa_acte_add'),
    path('empactelist/', views.empresaActividadEconomicaList, name='empresa_acte_list'),
    path('empacteedit/<int:id>', views.empresaActividadEconomicaEdit, name='empresa_acte_edit'),
    path('empacteview/<int:id>', views.empresaActividadEconomicaView, name='empresa_acte_view'),

#####################################
    path('empcert/postajax/', views.postEmpresaCertificacion, name = "empresa_cert_postajax"),
    path('empcert/postajaxdel/<int:id>', views.deleteEmpresaCertificacion, name = "empresa_cert_postajax_del"),

    path('empcertadd/', views.empresaCertificacionAdd, name='empresa_cert_add'),
    path('empcertlist/', views.empresaCertificacionList, name='empresa_cert_list'),
    path('empcertedit/<int:id>', views.empresaCertificacionEdit, name='empresa_cert_edit'),
    path('empcertview/<int:id>', views.empresaCertificacionView, name='empresa_cert_view'),


#####################################
    path('empdoc/postajax/', views.postEmpresaDocumentacion, name = "empresa_doc_postajax"),
    path('empdoc/postajaxdel/<int:id>', views.deleteEmpresaDocumentacion, name = "empresa_doc_postajax_del"),

    path('empdocadd/', views.empresaDocumentacionAdd, name='empresa_doc_add'),
    path('empdoclist/', views.empresaDocumentacionList, name='empresa_doc_list'),
    path('empdocedit/<int:id>', views.empresaDocumentacionEdit, name='empresa_doc_edit'),
    path('empdocview/<int:id>', views.empresaDocumentacionView, name='empresa_doc_view'),

#############################
    path('empredes/postajax/', views.postEmpresaRedSocial, name = "empresa_redes_postajax"),
    path('empredes/postajaxdel/<int:id>', views.deleteEmpresaRedSocial, name = "empresa_redes_postajax_del"),

    path('empredesadd/', views.empresaRedSocialAdd, name='empresa_redes_add'),
    path('empredeslist/', views.empresaRedSocialList, name='empresa_redes_list'),
    path('empredesedit/<int:id>', views.empresaRedSocialEdit, name='empresa_redes_edit'),
    path('empredesview/<int:id>', views.empresaRedSocialView, name='empresa_redes_view'),

    path('emprubro/postajax/', views.postEmpresaRubro, name = "empresa_rubro_postajax"),
    path('emprubro/postajaxdel/<int:id>', views.deleteEmpresaRubro, name = "empresa_rubro_postajax_del"),

    path('emprubroadd/', views.empresaRubroAdd, name='empresa_rubro_add'),
    path('emprubrolist/', views.empresaRubroList, name='empresa_rubro_list'),
    path('emprubroedit/<int:id>', views.empresaRubroEdit, name='empresa_rubro_edit'),
    path('emprubroview/<int:id>', views.empresaRubroView, name='empresa_rubro_view'),
    path('emprubrotags/', views.TagsJSONGet, name='empresa_rubro_tags'),
    


    #Experiencia
    path('empexp/postajax/', views.postEmpresaExperiencia, name = "empresa_exp_postajax"),
    path('empexp/postajaxdel/<int:id>', views.deleteEmpresaExperiencia, name = "empresa_exp_postajax_del"),

    path('empexpadd/', views.empresaExperienciaAdd, name='empresa_exp_add'),
    path('empexplist/', views.empresaExperienciaList, name='empresa_exp_list'),
    path('empexpedit/<int:id>', views.empresaExperienciaEdit, name='empresa_exp_edit'),
    path('empexpview/<int:id>', views.empresaExperienciaView, name='empresa_exp_view'),
    path('empexpfiles/<int:id>', views.empresaExperienciaSustentos, name='empresa_exp_files'),
    path('empexpfilesadd/<int:id>', views.empresaExperienciaSustentosAdd, name='empresa_exp_files_add'),
    path('empexpfilesdel/<int:id>', views.empresaExperienciaSustentosDelete, name='empresa_exp_files_del'),

    

] 