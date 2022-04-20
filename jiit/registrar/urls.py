from django.urls import path
from registrar import views

urlpatterns = [
    path('registrar', views.registrar, name='registrar'),
    path('registrar/registrarLogin', views.registrarLogin, name='rlogin'),
    path('registrar/registrarLogout', views.registrarLogout, name='rlogout'),
    
]