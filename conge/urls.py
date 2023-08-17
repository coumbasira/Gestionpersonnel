from django.urls import path
from . import views

urlpatterns = [
    path('', views.liste, name='liste'),
    path('chef/', views.chef, name='chef'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('demande_conge/', views.demande_conge, name='demande_conge'),
    path('valider_demande/<int:demande_id>/', views.valider_demande, name='valider_demande'),
]
