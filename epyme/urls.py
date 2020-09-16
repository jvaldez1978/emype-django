"""epyme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comun/', include(('apps.comun.urls', 'comun'), namespace='comun')),
	path('core/', include(('apps.core.urls', 'core'), namespace='core')),

    path('login/', LoginView.as_view(template_name='core/login.html'), name="login"),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name="logout"),
    path('reset/password_reset', PasswordResetView.as_view(), 
        {'template_name':'core/password_reset_form.html',
        'email_template_name': 'core/password_reset_email.html'}, 
        name='password_reset'), 
    path('password_reset_done', PasswordResetDoneView.as_view(), 
        {'template_name': 'core/password_reset_done.html'},
        name='password_reset_done'),
    path('reset/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), 
        {'template_name': 'core/password_reset_confirm.html'},
        name='password_reset_confirm'
        ),
    path('reset/done', PasswordResetCompleteView.as_view(), {'template_name': 'core/password_reset_complete.html'},
        name='password_reset_complete'),
    path('password_change', PasswordChangeView.as_view(), {'template_name': 'accounts/password_change.html'},
        name='password_change'),
    path('password_change_done', PasswordChangeDoneView.as_view(), {'template_name': 'accounts/password_change_done.html'},
        name='password_change_done') 

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
