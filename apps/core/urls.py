   
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [    
	path('registro/', views.signup, name='registro'),
    path('activacion_enviada/', views.account_activation_sent, name='activacion_enviada'),
    path('activacion/<str:uidb64>/<str:token>/', views.activate, name='activacion'),
    path('activado/', views.account_activated, name='activado'),
    path('activacion_invalida/', views.account_activation_invalid, name='activacion_invalida'),
]
