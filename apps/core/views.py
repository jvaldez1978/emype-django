# views.py
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.shortcuts import get_object_or_404

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .tokens import account_activation_token
from django.contrib.auth import get_user_model

from apps.comun.models import  Empresa, EmpresaUsuario, PerfilUsuario, EmpresaRepresentante, EmpresaLocacion, EmpresaRedSocial, EmpresaActividadEconomica, EmpresaCertificacion, EmpresaExperiencia, EmpresaExperienciaDocumentacion, EmpresaRubro, Tags


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.username = user.email
            user.save()
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta en eMYPE'
            message = render_to_string('core/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('core:activacion_enviada')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})    

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if user.email_confirmed == False:
            user.is_active = True
            user.email_confirmed = True
            user.save()
            login(request, user)
            return redirect('core:activado')
    return render(request, 'core/account_activation_invalid.html')

def account_activation_sent(request):
    return render(request, 'core/account_activation_sent.html')

def account_activated(request):
    return render(request, 'core/account_activated.html')

def account_activation_invalid(request):
    return render(request, 'core/account_activation_invalid.html')

def verifica_empresa(function):
    def _function(request,*args, **kwargs):
        empresaUsuario = EmpresaUsuario.objects.filter(usuario = request.user.id).first()
        if empresaUsuario == None:
            return HttpResponseRedirect('/comun/empadd/')
        return function(request, *args, **kwargs)
    return _function

def verifica_permiso_usuario_empresa(function, model):
    def _function(request, id, *args, **kwargs):        
        empresaRepresentante = get_object_or_404(EmpresaRepresentante, id = id)
        row = get_object_or_404(EmpresaUsuario, usuario = request.user.id)
        if row.empresa_id != empresaRepresentante.empresa_id:
            raise Http404()
            return HttpResponseRedirect('/comun/empadd/')
        return function(request, *args, **kwargs)
    return _function