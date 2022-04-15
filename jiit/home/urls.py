from unicodedata import name
from django.urls import path
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name="login"),
    path('loginCheck', views.loginCheck, name="loginCheck"),
    path('logout', views.logout, name='logout'),
    path('signUp', views.signUp, name='signUp'),
    path('signUpCheck', views.signUpCheck, name='signUpCheck'),
]