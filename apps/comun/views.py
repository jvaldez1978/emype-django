from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.http import JsonResponse
from django.core import serializers
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

import json
import decimal
from datetime import datetime, timedelta
from django.utils import timezone

def error_404(request, exception):
        data = {}
        return render(request,'404.html', data)

def error_500(request,  exception):
        data = {}
        return render(request,'500.html', data)
 

# Create your views here.
def index(request):
    return render(request, 'comun/empresa_edit.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from .forms import ImageUploadForm, empForm, empNuevaForm, empresaRepresentanteForm, empresaLocacionForm, empresaRedSocialForm, empresaActividadEconomicaForm, empresaCertificacionForm, empresaExperienciaForm, empresaExperienciaSustentoForm, empresaRubroForm, empEditarForm, empresaLocacionFotoForm, empresaDocumentacionForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Empresa, EmpresaUsuario, PerfilUsuario, EmpresaRepresentante, EmpresaLocacion, EmpresaRedSocial, EmpresaActividadEconomica, EmpresaCertificacion, EmpresaExperiencia, EmpresaExperienciaDocumentacion, EmpresaRubro, Tags, EmpresaLocacionFotoTicket, EmpresaDocumentacion
from apps.core.views import verifica_empresa, verifica_permiso_usuario_empresa

def verificaEmpresaUsuario(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    return empresaUsuario

@login_required
def obtieneEmpresa(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    data = {}
    if empresaUsuario != None:
        empresa_nombre = empresaUsuario.empresa.razon_social
        data = {'empresa': empresa_nombre }
    return JsonResponse(data)

@login_required
def empresaAdd(request):
    if request.method =="POST":
        formA = empNuevaForm(request.POST)
        if formA.is_valid():# and formB.is_valid() and formC.is_valid():
            fa = formA.save()            
            perfilAdministrador = PerfilUsuario.objects.filter(nombre='Administrador').first()
            empresaUsuario = EmpresaUsuario(empresa_id=fa.id, perfil_id=perfilAdministrador.id, usuario_id=request.user.id)
            empresaUsuario.save()
        return redirect(reverse('comun:empresa_view'))
    else:
        formA = empNuevaForm(prefix = 'emp')
        empresa_nombre = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_nombre = empresaUsuario.empresa.razon_social
        args = {'formA' : formA}#, 'formB' : formB, 'formC' : formC}
        return render(request, 'comun/empresa_add.html', args)

@login_required
@verifica_empresa
def empresaEdit(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    empresa_ok = False
    if empresaUsuario != None:
        empresa_ok = True
        empresa = Empresa.objects.get(id=empresaUsuario.empresa_id)
    else:
        return redirect(reverse('comun:empresa_add'))

    if request.method =="POST":
        formA = empEditarForm(request.POST, prefix = 'emp', instance = empresa)
        
        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():           
            empresa = formA.save(commit = False)
            #fa = formA.save(commit = False)
            #fa.empresa_id = empresaUsuario.empresa_id
            empresa.save()
        return redirect(reverse('comun:empresa_view'))
    else:
        formA = empEditarForm(instance = empresa, prefix = 'emp')
        empresa_nombre = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_nombre = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa_nombre, 'id_row': empresa.id}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_edit.html', args)    

@login_required
def postEmpresa(request):
    # request should be ajax and method should be POST.
    print('1')
    if request.is_ajax and request.method == "POST":
        print('2')
        # get the form data
        id_row = None
        if ('id_row' in request.POST.keys()):
            id_row = request.POST['id_row'] 

        if id_row != None:
            form = empEditarForm(request.POST, prefix = 'emp', instance=Empresa.objects.get(id=id_row))
        else:
            form = empNuevaForm(request.POST, prefix = 'emp')
        # save the data and after fetch the object in instance
        #verificacion = verificaEmpresaUsuario(request)

        if form.is_valid():            
            print('3')
            if id_row != None:
                print('4')
                form = empEditarForm(request.POST, prefix = 'emp', instance=Empresa.objects.get(id=id_row))
                instance = form.save()
            else:
                print('5')
                instance = form.save()
                perfilAdministrador = PerfilUsuario.objects.filter(nombre='Administrador').first()
                empresaUsuario = EmpresaUsuario(empresa_id=instance.id, perfil_id=perfilAdministrador.id, usuario_id=request.user.id)
                empresaUsuario.save()

            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": form.errors}, status=400)

    # some error occured
    return JsonResponse({"errors": ""}, status=400)

@login_required
@verifica_empresa
def empresaView(request):
    empresa_nombre = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    if empresaUsuario != None:
        empresa_nombre = empresaUsuario.empresa.razon_social
        empresa = Empresa.objects.get(id = empresaUsuario.empresa_id)
        formA = empNuevaForm(instance = empresa)

    args = {'formA' : formA, 'empresa': empresa_nombre }#, 'formB' : formB, 'formC' : formC}
    
    return render(request, 'comun/empresa_view.html', args)

@login_required
@verifica_empresa
def empresaHome(request):
    empresa = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    if empresaUsuario != None:
        empresa = empresaUsuario.empresa.razon_social
        url = 'comun/empresa_home.html'
    else:
        url = 'comun/empresa_empty.html'
    args = {'empresa': empresa}
    return render(request, url, args)

################################################################

@login_required
@verifica_empresa
def empresaRepresentanteAdd(request):
    if request.method =="POST":
        formA = empresaRepresentanteForm(request.POST)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():            
            fa = formA.save(commit = False)
            fa.empresa_id = empresaUsuario.empresa_id
            fa.save()
        return redirect(reverse('comun:empresa_rep_list'))
    else:
        formA = empresaRepresentanteForm()
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_rep_add.html', args)    


@login_required
@verifica_empresa
def postRepresentanteEmpresa(request):
    # request should be ajax and method should be POST.
    print(request.POST)
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = empresaRepresentanteForm(request.POST)
        # save the data and after fetch the object in instance
        verificacion = verificaEmpresaUsuario(request)

        id_row = None
        if ('id_row' in request.POST.keys()):
            id_row = request.POST['id_row'] 

        if form.is_valid() and verificacion != None:            
            if id_row != None:
                form = empresaRepresentanteForm(request.POST, instance=EmpresaRepresentante.objects.get(id=id_row))
                instance = form.save()
            else:
                instance = form.save(commit = False)
                instance.empresa_id = verificacion.empresa_id
                instance.save()

            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": form.errors}, status=400)

    # some error occured
    return JsonResponse({"errors": ""}, status=400)

@login_required
@verifica_empresa
def deleteRepresentanteEmpresa(request, id):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "DELETE":
        # get the form data        
        verificacion = verificaEmpresaUsuario(request)

        if verificacion != None:            
            empresaRepresentante = EmpresaRepresentante.objects.get(id = id)
            empresaRepresentante.delete()

            # send to client side.
            return JsonResponse({"data": 'Registro eliminado satisfactoriamente'}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": 'Defición de empresa invalida'}, status=400)

    # some error occured
    return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)

@login_required
@verifica_empresa
def empresaRepresentanteList(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    empresaRepresentantes = None
    if  empresaUsuario!= None:
        empresaRepresentantes = EmpresaRepresentante.objects.filter(empresa__id=empresaUsuario.empresa_id)    
    return render(request, 'comun/empresa_rep_list.html', {"representantes": empresaRepresentantes})

@login_required
@verifica_empresa
#@verifica_permiso_usuario_empresa(EmpresaRepresentante)
def empresaRepresentanteEdit(request, id):
    empresaRepresentante = get_object_or_404(EmpresaRepresentante, id = id)

    #verifica si la informacion    
    empresaUsuario = get_object_or_404(EmpresaUsuario, usuario = request.user.id)
    if empresaUsuario.empresa_id != empresaRepresentante.empresa_id:
        raise Http404()

    formA = empresaRepresentanteForm(instance = empresaRepresentante)    

    # NO OLVIDAR ENVIAR ID_ROW, NECESARIO PARA IDENTIFICAR EL REGISTRO A EDITAR
    args = {'formA' : formA, 'id_row': empresaRepresentante.id}
    return render(request, 'comun/empresa_rep_edit.html', args) 

@login_required
@verifica_empresa
def empresaRepresentanteView(request, id):
    empresaRepresentante = EmpresaRepresentante.objects.get(id=id)
    formA = empresaRepresentanteForm(instance = empresaRepresentante)
    empresa = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    if empresaUsuario != None:
        empresa = empresaUsuario.empresa.razon_social
    args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
    
    return render(request, 'comun/empresa_rep_view.html', args)    

########################################

@login_required
@verifica_empresa
def postEmpresaLocacion(request):
    # request should be ajax and method should be POST.
    #print(request.POST['id_row'])
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = empresaLocacionForm(request.POST)
        # save the data and after fetch the object in instance
        verificacion = verificaEmpresaUsuario(request)

        id_row = None
        if ('id_row' in request.POST.keys()):
            id_row = request.POST['id_row'] 

        if form.is_valid() and verificacion != None:            
            if id_row != None:
                form = empresaLocacionForm(request.POST, instance=EmpresaLocacion.objects.get(id=id_row))
                instance = form.save()
            else:
                instance = form.save(commit = False)
                instance.empresa_id = verificacion.empresa_id
                instance.save()

            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": form.errors}, status=400)

    # some error occured
    return JsonResponse({"errors": ""}, status=400)

@login_required
@verifica_empresa
def deleteEmpresaLocacion(request, id):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "DELETE":
        # get the form data        
        verificacion = verificaEmpresaUsuario(request)

        if verificacion != None:            
            empresaLocacion = EmpresaLocacion.objects.get(id = id)
            empresaLocacion.delete()

            # send to client side.
            return JsonResponse({"data": 'Registro eliminado satisfactoriamente'}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": 'Defición de empresa invalida'}, status=400)

    # some error occured
    return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)

def pruebafoto(request, envio_id):
    print(request.method)
    args = {'mensaje' : ''}    
    if request.method == "POST":        
        form = ImageUploadForm(request.POST, request.FILES)
        empresaLocacionFotoTicket = get_object_or_404(EmpresaLocacionFotoTicket, envio_id = envio_id)
        d = timedelta(days=1)

        if form.is_valid() and empresaLocacionFotoTicket.usado!=True and timezone.now() < empresaLocacionFotoTicket.fecha + d:
            empresaLocacionFotoTicket.usado = True
            empresaLocacion = EmpresaLocacion.objects.get(id = empresaLocacionFotoTicket.empresa_locacion_id)
            empresaLocacion.foto = form.cleaned_data['foto']
            empresaLocacion.save()
            empresaLocacionFotoTicket.save()
            args = {'mensaje' : 'Foto enviada!'}   
        else:
             args = {'mensaje' : 'Error al enviar la foto!'}   
        #return redirect(reverse('comun:empresa_loc_list'))  
    return render(request, 'comun/empresa_loc_fotos.html', args)    

@login_required
@verifica_empresa
def postEmpresaLocacionFoto(request, id):
    # request should be ajax and method should be POST.
    try:
        if request.is_ajax and request.method == "POST":
            # get the form data        
            verificacion = verificaEmpresaUsuario(request)

            if verificacion != None:            
                empresaLocacion = EmpresaLocacion.objects.get(id = id)
                ticket = EmpresaLocacionFotoTicket(empresa_locacion_id = id)
                ticket.save()
 
                subject, from_email, to = 'Foto de sede para plataforma eMYPE', 'portal.emype@gmail.com', request.user.email
                text_content = ''
                html_content = '<p>El siguiente link lo llevara a una pagina donde debera tomar una foto para evidenciar ubicacion de la sede.</p><br><a href="'+request.build_absolute_uri(reverse('comun:pruebafoto', args=[ticket.envio_id]))+'" target="_blank">Haga click aqui</a>'
                msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()     

                # send to client side.
                return JsonResponse({"data": 'Registro eliminado satisfactoriamente'}, status=200)
            else:
                # some form errors occured.
                return JsonResponse({"errors": 'Defición de empresa invalida'}, status=400)

        # some error occured
        return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)
    except:
        return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)


@login_required
@verifica_empresa
def empresaLocacionAdd(request):
    if request.method =="POST":
        formA = empresaLocacionForm(request.POST)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():            
            fa = formA.save(commit = False)
            fa.empresa_id = empresaUsuario.empresa_id
            fa.save()
        return redirect(reverse('comun:empresa_loc_list'))
    else:
        formA = empresaLocacionForm()
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_loc_add.html', args)    

@login_required
@verifica_empresa
def empresaLocacionList(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    empresaRepresentantes = None
    if  empresaUsuario!= None:
        empresaLocacion = EmpresaLocacion.objects.filter(empresa__id=empresaUsuario.empresa_id)    
    return render(request, 'comun/empresa_loc_list.html', {"locaciones": empresaLocacion})

@login_required
@verifica_empresa
def empresaLocacionEdit(request, id):
    empresaLocacion = EmpresaLocacion.objects.get(id=id)

    if request.method =="POST":
        formA = empresaLocacionForm(request.POST, instance = empresaLocacion)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():           
            empresaLocacion = formA.save(commit = False)
            #fa = formA.save(commit = False)
            #fa.empresa_id = empresaUsuario.empresa_id
            empresaLocacion.save()
        return redirect(reverse('comun:empresa_loc_list'))
    else:
        formA = empresaLocacionForm(instance = empresaLocacion)
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        empresaLocacion = EmpresaLocacion.objects.get(id=id)
        locations = [
            [empresaLocacion.id, empresaLocacion.latitud, empresaLocacion.longitud, 1]            
        ]
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa, 'id_row': empresaLocacion.id, 'locations': json.dumps(locations, cls=DecimalEncoder)}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_loc_edit.html', args)    

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)

@login_required
@verifica_empresa
def empresaLocacionView(request, id):
    empresaLocacion = EmpresaLocacion.objects.get(id=id)
    formA = empresaLocacionForm(instance = empresaLocacion)
    empresa = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    if empresaUsuario != None:
        empresa = empresaUsuario.empresa.razon_social
    empresaLocacion = EmpresaLocacion.objects.get(id=id)
    locations = [
        [empresaLocacion.id, empresaLocacion.latitud, empresaLocacion.longitud, 1]            
    ]
    foto_url = "#"
    if empresaLocacion.foto:
        foto_url = empresaLocacion.foto.url
    args = {'formA' : formA, 'empresa': empresa,'locations': json.dumps(locations, cls=DecimalEncoder), 'foto_url': foto_url}#, 'formB' : formB, 'formC' : formC}    
    return render(request, 'comun/empresa_loc_view.html', args)    

@login_required
@verifica_empresa
def LocacionJSONGet(request, id):    
    locations = [
        [l.id, l.latitud, l.longitud, i]
        for i, l in enumerate(locacion = EmpresaLocacion.objects.filter(id=id))
    ]
    #serializer = TagsSerializer(tags, many=True)
    #json_data = json.dumps(locations)
    #tags_list = json.dumps(list(tags), cls=DjangoJSONEncoder)
    return JsonResponse(json.dumps(locations), safe=False)

########################################
@login_required
@verifica_empresa
def empresaActividadEconomicaAdd(request):
    if request.method =="POST":
        formA = empresaActividadEconomicaForm(request.POST)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():            
            fa = formA.save(commit = False)
            fa.empresa_id = empresaUsuario.empresa_id
            fa.save()
        return redirect(reverse('comun:empresa_acte_list'))
    else:
        formA = empresaActividadEconomicaForm()
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_acte_add.html', args)    

@login_required
@verifica_empresa
def empresaActividadEconomicaList(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    empresaActividadEconomica = None
    if  empresaUsuario!= None:
        empresaActividadEconomica = EmpresaActividadEconomica.objects.filter(empresa__id=empresaUsuario.empresa_id)    
    return render(request, 'comun/empresa_acte_list.html', {"actividades_economicas": empresaActividadEconomica})

@login_required
@verifica_empresa
def empresaActividadEconomicaEdit(request, id):
    empresaActividadEconomica = EmpresaActividadEconomica.objects.get(id=id)

    if request.method =="POST":
        formA = empresaActividadEconomicaForm(request.POST, instance = empresaActividadEconomica)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():           
            empresaActividadEconomica = formA.save(commit = False)
            #fa = formA.save(commit = False)
            #fa.empresa_id = empresaUsuario.empresa_id
            empresaActividadEconomica.save()
        return redirect(reverse('comun:empresa_acte_list'))
    else:
        formA = empresaActividadEconomicaForm(instance = empresaActividadEconomica)
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_acte_edit.html', args)    

@login_required
@verifica_empresa
def empresaActividadEconomicaView(request, id):
    empresaActividadEconomica = EmpresaActividadEconomica.objects.get(id=id)
    formA = empresaActividadEconomicaForm(instance = empresaActividadEconomica)
    empresa = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    if empresaUsuario != None:
        empresa = empresaUsuario.empresa.razon_social
    args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
    
    return render(request, 'comun/empresa_acte_view.html', args)    


########################################
@login_required
@verifica_empresa
def postEmpresaRedSocial(request):
    # request should be ajax and method should be POST.
    #print(request.POST['id_row'])
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = empresaRedSocialForm(request.POST)
        # save the data and after fetch the object in instance
        verificacion = verificaEmpresaUsuario(request)

        id_row = None
        if ('id_row' in request.POST.keys()):
            id_row = request.POST['id_row'] 

        if form.is_valid() and verificacion != None:            
            if id_row != None:
                form = empresaRedSocialForm(request.POST, instance=EmpresaRedSocial.objects.get(id=id_row))
                instance = form.save()
            else:
                instance = form.save(commit = False)
                instance.empresa_id = verificacion.empresa_id
                instance.save()

            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": form.errors}, status=400)

    # some error occured
    return JsonResponse({"errors": ""}, status=400)

@login_required
@verifica_empresa
def deleteEmpresaRedSocial(request, id):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "DELETE":
        # get the form data        
        verificacion = verificaEmpresaUsuario(request)

        if verificacion != None:            
            empresaRedSocial = EmpresaRedSocial.objects.get(id = id)
            empresaRedSocial.delete()

            # send to client side.
            return JsonResponse({"data": 'Registro eliminado satisfactoriamente'}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": 'Defición de empresa invalida'}, status=400)

    # some error occured
    return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)


@login_required
@verifica_empresa
def empresaRedSocialAdd(request):
    if request.method =="POST":
        formA = empresaRedSocialForm(request.POST)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():            
            fa = formA.save(commit = False)
            fa.empresa_id = empresaUsuario.empresa_id
            fa.save()
        return redirect(reverse('comun:empresa_redes_list'))
    else:
        formA = empresaRedSocialForm()
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_redes_add.html', args)    

@login_required
@verifica_empresa
def empresaRedSocialList(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    empresaRedSocial = None
    if  empresaUsuario!= None:
        empresaRedSocial = EmpresaRedSocial.objects.filter(empresa__id=empresaUsuario.empresa_id)    
    return render(request, 'comun/empresa_redes_list.html', {"redes_sociales": empresaRedSocial})

@login_required
@verifica_empresa
def empresaRedSocialEdit(request, id):
    empresaRedSocial = EmpresaRedSocial.objects.get(id=id)

    if request.method =="POST":
        formA = empresaRedSocialForm(request.POST, instance = empresaRedSocial)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():           
            empresaRedSocial = formA.save(commit = False)
            #fa = formA.save(commit = False)
            #fa.empresa_id = empresaUsuario.empresa_id
            empresaRedSocial.save()
        return redirect(reverse('comun:empresa_redes_list'))
    else:
        formA = empresaRedSocialForm(instance = empresaRedSocial)
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa, 'id_row': empresaRedSocial.id}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_redes_edit.html', args)    

@login_required
@verifica_empresa
def empresaRedSocialView(request, id):
    empresaRedSocial = EmpresaRedSocial.objects.get(id=id)
    formA = empresaRedSocialForm(instance = empresaRedSocial)
    empresa = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    if empresaUsuario != None:
        empresa = empresaUsuario.empresa.razon_social
    args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
    
    return render(request, 'comun/empresa_redes_view.html', args)    

########################################

@login_required
@verifica_empresa
def postEmpresaCertificacion(request):
    # request should be ajax and method should be POST.
    print(request.POST)
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = empresaCertificacionForm(request.POST, request.FILES)
        
        # save the data and after fetch the object in instance
        verificacion = verificaEmpresaUsuario(request)

        id_row = None
        if ('id_row' in request.POST.keys()):
            id_row = request.POST['id_row'] 

        print('0')
        if form.is_valid() and verificacion != None:            
            print('1')
            if id_row != None:
                print('2')
                form = empresaCertificacionForm(request.POST, request.FILES, instance=EmpresaCertificacion.objects.get(id=id_row))
                instance = form.save()
            else:
                instance = form.save(commit = False)
                instance.empresa_id = verificacion.empresa_id
                instance.save()

            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": form.errors}, status=400)

    # some error occured
    return JsonResponse({"errors": ""}, status=400)

@login_required
@verifica_empresa
def deleteEmpresaCertificacion(request, id):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "DELETE":
        # get the form data        
        verificacion = verificaEmpresaUsuario(request)

        if verificacion != None:            
            empresaCertificacion = EmpresaCertificacion.objects.get(id = id)
            empresaCertificacion.delete()

            # send to client side.
            return JsonResponse({"data": 'Registro eliminado satisfactoriamente'}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": 'Defición de empresa invalida'}, status=400)

    # some error occured
    return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)


@login_required
@verifica_empresa
def empresaCertificacionAdd(request):
    if request.method =="POST":
        formA = empresaCertificacionForm(request.POST)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():            
            fa = formA.save(commit = False)
            fa.empresa_id = empresaUsuario.empresa_id
            fa.save()
        return redirect(reverse('comun:empresa_cert_list'))
    else:
        formA = empresaCertificacionForm()
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_cert_add.html', args)    

@login_required
@verifica_empresa
def empresaCertificacionList(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    empresaCertificacion = None
    if  empresaUsuario!= None:
        empresaCertificacion = EmpresaCertificacion.objects.filter(empresa__id=empresaUsuario.empresa_id)    
    return render(request, 'comun/empresa_cert_list.html', {"certificaciones": empresaCertificacion})

@login_required
@verifica_empresa
def empresaCertificacionEdit(request, id):
    empresaCertificacion = EmpresaCertificacion.objects.get(id=id)

    if request.method =="POST":
        formA = empresaCertificacionForm(request.POST, instance = empresaCertificacion)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():           
            empresaCertificacion = formA.save(commit = False)
            #fa = formA.save(commit = False)
            #fa.empresa_id = empresaUsuario.empresa_id
            empresaCertificacion.save()
        return redirect(reverse('comun:empresa_cert_list'))
    else:
        formA = empresaCertificacionForm(instance = empresaCertificacion)
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'id_row' : empresaCertificacion.id }#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_cert_edit.html', args)    

@login_required
@verifica_empresa
def empresaCertificacionView(request, id):
    empresaCertificacion = EmpresaCertificacion.objects.get(id=id)
    formA = empresaCertificacionForm(instance = empresaCertificacion)
    empresa = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    if empresaUsuario != None:
        empresa = empresaUsuario.empresa.razon_social
    args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
    
    return render(request, 'comun/empresa_cert_view.html', args)    

########################################

@login_required
@verifica_empresa
def postEmpresaDocumentacion(request):
    # request should be ajax and method should be POST.
    print(request.POST)
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = empresaDocumentacionForm(request.POST, request.FILES)
        
        # save the data and after fetch the object in instance
        verificacion = verificaEmpresaUsuario(request)

        id_row = None
        if ('id_row' in request.POST.keys()):
            id_row = request.POST['id_row'] 

        print('0')
        if form.is_valid() and verificacion != None:            
            print('1')
            if id_row != None:
                print('2')
                form = empresaDocumentacionForm(request.POST, request.FILES, instance=EmpresaDocumentacion.objects.get(id=id_row))
                instance = form.save()
            else:
                instance = form.save(commit = False)
                instance.empresa_id = verificacion.empresa_id
                instance.save()

            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": form.errors}, status=400)

    # some error occured
    return JsonResponse({"errors": ""}, status=400)

@login_required
@verifica_empresa
def deleteEmpresaDocumentacion(request, id):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "DELETE":
        # get the form data        
        verificacion = verificaEmpresaUsuario(request)

        if verificacion != None:            
            empresaDocumentacion = EmpresaDocumentacion.objects.get(id = id)
            empresaDocumentacion.delete()

            # send to client side.
            return JsonResponse({"data": 'Registro eliminado satisfactoriamente'}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": 'Defición de empresa invalida'}, status=400)

    # some error occured
    return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)


@login_required
@verifica_empresa
def empresaDocumentacionAdd(request):
    if request.method =="POST":
        formA = empresaDocumentacionForm(request.POST)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():            
            fa = formA.save(commit = False)
            fa.empresa_id = empresaUsuario.empresa_id
            fa.save()
        return redirect(reverse('comun:empresa_doc_list'))
    else:
        formA = empresaDocumentacionForm()
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_doc_add.html', args)    

@login_required
@verifica_empresa
def empresaDocumentacionList(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    empresaDocumentacion = None
    if  empresaUsuario!= None:
        empresaDocumentacion = EmpresaDocumentacion.objects.filter(empresa__id=empresaUsuario.empresa_id)    
    return render(request, 'comun/empresa_doc_list.html', {"certificaciones": empresaDocumentacion})

@login_required
@verifica_empresa
def empresaDocumentacionEdit(request, id):
    empresaDocumentacion = EmpresaDocumentacion.objects.get(id=id)

    if request.method =="POST":
        formA = empresaDocumentacionForm(request.POST, instance = empresaDocumentacion)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():           
            empresaDocumentacion = formA.save(commit = False)
            #fa = formA.save(commit = False)
            #fa.empresa_id = empresaUsuario.empresa_id
            empresaDocumentacion.save()
        return redirect(reverse('comun:empresa_doc_list'))
    else:
        formA = empresaDocumentacionForm(instance = empresaDocumentacion)
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'id_row' : empresaDocumentacion.id }#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_doc_edit.html', args)    

@login_required
@verifica_empresa
def empresaDocumentacionView(request, id):
    empresaDocumentacion = EmpresaDocumentacion.objects.get(id=id)
    formA = empresaDocumentacionForm(instance = empresaDocumentacion)
    empresa = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    if empresaUsuario != None:
        empresa = empresaUsuario.empresa.razon_social
    args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
    
    return render(request, 'comun/empresa_doc_view.html', args)    

########################################

@login_required
@verifica_empresa
def postEmpresaExperiencia(request):
    # request should be ajax and method should be POST.
    #print(request.POST['id_row'])
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = empresaExperienciaForm(request.POST)
        # save the data and after fetch the object in instance
        verificacion = verificaEmpresaUsuario(request)

        id_row = None
        if ('id_row' in request.POST.keys()):
            id_row = request.POST['id_row'] 

        if form.is_valid() and verificacion != None:            
            if id_row != None:
                form = empresaExperienciaForm(request.POST, instance=EmpresaExperiencia.objects.get(id=id_row))
                instance = form.save()
            else:
                instance = form.save(commit = False)
                instance.empresa_id = verificacion.empresa_id
                instance.save()

            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": form.errors}, status=400)

    # some error occured
    return JsonResponse({"errors": ""}, status=400)

@login_required
@verifica_empresa
def deleteEmpresaExperiencia(request, id):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "DELETE":
        # get the form data        
        verificacion = verificaEmpresaUsuario(request)

        if verificacion != None:            
            empresaExperiencia = EmpresaExperiencia.objects.get(id = id)
            try:
                empresaExperiencia.delete()
            except ProtectedError:
                return JsonResponse({"errors": "El registro tiene sustentos asociados y no se puede eliminar"}, status=400)
            
            # send to client side.
            return JsonResponse({"data": 'Registro eliminado satisfactoriamente'}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": 'Defición de empresa invalida'}, status=400)

    # some error occured
    return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)


@login_required
@verifica_empresa
def empresaExperienciaAdd(request):
    if request.method =="POST":
        formA = empresaExperienciaForm(request.POST)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():            
            fa = formA.save(commit = False)
            fa.empresa_id = empresaUsuario.empresa_id
            fa.save()
        return redirect(reverse('comun:empresa_exp_list'))
    else:
        formA = empresaExperienciaForm()
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_exp_add.html', args)    

@login_required
@verifica_empresa
def empresaExperienciaList(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    empresaExperiencia = None
    if  empresaUsuario!= None:
        empresaExperiencia = EmpresaExperiencia.objects.filter(empresa__id=empresaUsuario.empresa_id)    
    return render(request, 'comun/empresa_exp_list.html', {"experiencia": empresaExperiencia})

@login_required
@verifica_empresa
def empresaExperienciaEdit(request, id):
    empresaExperiencia = EmpresaExperiencia.objects.get(id=id)

    if request.method =="POST":
        formA = empresaExperienciaForm(request.POST, instance = empresaExperiencia)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():           
            empresaExperiencia = formA.save(commit = False)
            #fa = formA.save(commit = False)
            #fa.empresa_id = empresaUsuario.empresa_id
            empresaExperiencia.save()
        return redirect(reverse('comun:empresa_exp_list'))
    else:
        formA = empresaExperienciaForm(instance = empresaExperiencia)
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa, 'id_row': empresaExperiencia.id}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_exp_edit.html', args)    

@login_required
@verifica_empresa
def empresaExperienciaView(request, id):
    empresaExperiencia = EmpresaExperiencia.objects.get(id=id)
    formA = empresaExperienciaForm(instance = empresaExperiencia)
    empresa = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    if empresaUsuario != None:
        empresa = empresaUsuario.empresa.razon_social
    args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
    
    return render(request, 'comun/empresa_exp_view.html', args)    

@login_required
@verifica_empresa
def empresaExperienciaSustentos(request, id):
    empresaExperienciaDocumentacion = EmpresaExperienciaDocumentacion.objects.filter(empresa_experiencia__id=id)    
    form = empresaExperienciaSustentoForm()
    return render(request, 'comun/empresa_exp_sustentos_partial.html', {"sustentos": empresaExperienciaDocumentacion, 'form': form, 'id': id })
        
@login_required
@verifica_empresa
def empresaExperienciaSustentosAdd(request, id):
    print('1')
    if request.method == 'POST':        
        data = {'resultado' : 'error'}
        print('2')
        form = empresaExperienciaSustentoForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            print('3')
            sustento = form.save(commit=False)
            sustento.empresa_experiencia_id = id
            sustento.save() 
            data = {'resultado': 'ok' }
        return HttpResponseRedirect('/comun/empexplist/')

@login_required
@verifica_empresa
def empresaExperienciaSustentosDelete(request, id):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "DELETE":
        # get the form data        
        verificacion = verificaEmpresaUsuario(request)

        if verificacion != None:            
            empresaExperienciaDocumentacion = EmpresaExperienciaDocumentacion.objects.get(id=id)
            empresaExperienciaDocumentacion.delete()

            # send to client side.
            return JsonResponse({"data": 'Registro eliminado satisfactoriamente'}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": 'Defición de empresa invalida'}, status=400)

    # some error occured
    return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)



########################################

@login_required
@verifica_empresa
def postEmpresaRubro(request):
    # request should be ajax and method should be POST.
    print(request.POST)
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = empresaRubroForm(request.POST)
        # save the data and after fetch the object in instance
        verificacion = verificaEmpresaUsuario(request)

        id_row = None
        if ('id_row' in request.POST.keys()):
            id_row = request.POST['id_row'] 

        if form.is_valid() and verificacion != None:            
            if id_row != None:
                form = empresaRubroForm(request.POST, instance=EmpresaRubro.objects.get(id=id_row))
                instance = form.save()
            else:
                instance = form.save(commit = False)
                instance.empresa_id = verificacion.empresa_id
                instance.save()

            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": form.errors}, status=400)

    # some error occured
    return JsonResponse({"errors": ""}, status=400)

@login_required
@verifica_empresa
def deleteEmpresaRubro(request, id):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "DELETE":
        # get the form data        
        verificacion = verificaEmpresaUsuario(request)

        if verificacion != None:            
            empresaRubro = EmpresaRubro.objects.get(id = id)
            empresaRubro.delete()

            # send to client side.
            return JsonResponse({"data": 'Registro eliminado satisfactoriamente'}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"errors": 'Defición de empresa invalida'}, status=400)

    # some error occured
    return JsonResponse({"errors": "Ocurrió un error inesperado"}, status=400)

@login_required
@verifica_empresa
def empresaRubroAdd(request):
    if request.method =="POST":
        formA = empresaRubroForm(request.POST)
        print(formA)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        #print(formA.rubro)
        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():            
            fa = formA.save(commit = False)
            fa.empresa_id = empresaUsuario.empresa_id
            fa.save()
        return redirect(reverse('comun:empresa_rubro_list'))
    else:
        formA = empresaRubroForm()
        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_rubro_add.html', args)    

@login_required
@verifica_empresa
def empresaRubroList(request):
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
    empresaRubro = None
    if  empresaUsuario!= None:
        empresaRubro = EmpresaRubro.objects.filter(empresa__id=empresaUsuario.empresa_id)    
    return render(request, 'comun/empresa_rubro_list.html', {"rubros": empresaRubro})

@login_required
@verifica_empresa
def empresaRubroEdit(request, id):
    empresaRubro = EmpresaRubro.objects.get(id=id)

    if request.method =="POST":
        formA = empresaRubroForm(request.POST, instance = empresaRubro)
        empresa_ok = False

        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa_ok = True

        if formA.is_valid() and empresa_ok:# and formB.is_valid() and formC.is_valid():           
            empresaRubro = formA.save(commit = False)
            #fa = formA.save(commit = False)
            #fa.empresa_id = empresaUsuario.empresa_id
            empresaRubro.save()
        return redirect(reverse('comun:empresa_rubro_list'))
    else:
        formA = empresaRubroForm(instance = empresaRubro)
        tags = Tags.objects.all()
        #serializer = TagsSerializer(tags, many=True)
        json_data = json.dumps([{'text': tag.nombre, 'value': tag.nombre} for tag in tags])
        tags_list = json.dumps(json_data, cls=DjangoJSONEncoder)
        #json_safe = JsonResponse(json_data, safe=False)

        empresa_json_tags = []
        empresaTags = empresaRubro.etiquetas.split(",")
        for tag in empresaTags:
            print('x')
            empresa_json_tags.append({"text": tag , "value": tag})

        empresa = ""
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
        if empresaUsuario != None:
            empresa = empresaUsuario.empresa.razon_social
        args = {'formA' : formA, 'id_row' : empresaRubro.id, 'tag_list' : json_data, 'empresa_json_tags': json.dumps(empresa_json_tags)}#, 'formB' : formB, 'formC' : formC}
        
        return render(request, 'comun/empresa_rubro_edit.html', args)    

@login_required
@verifica_empresa
def empresaRubroView(request, id):
    empresaRubro = EmpresaRubro.objects.get(id=id)
    formA = empresaRubroForm(instance = empresaRubro)
    empresa = ""
    empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()        
    if empresaUsuario != None:
        empresa = empresaUsuario.empresa.razon_social
    args = {'formA' : formA, 'empresa': empresa}#, 'formB' : formB, 'formC' : formC}
    
    return render(request, 'comun/empresa_rubro_view.html', args)    

import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required
@verifica_empresa
def TagsJSONGet(request):
    tags = Tags.objects.all()
    #serializer = TagsSerializer(tags, many=True)
    json_data = json.dumps([{'text': tag.nombre, 'value': tag.nombre} for tag in tags])
    #tags_list = json.dumps(list(tags), cls=DjangoJSONEncoder)
    return JsonResponse(json_data, safe=False)

