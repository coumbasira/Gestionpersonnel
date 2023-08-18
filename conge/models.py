from django.db import models
from django.contrib.auth.models import User



class CongeRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    motif = models.CharField(max_length=200)
    date_depart = models.DateField()
    date_arrivee = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'En attente'), ('approved', 'Approuvé'), ('rejected', 'Rejeté')], default='pending')

class ChefResponse(models.Model):
    request = models.ForeignKey(CongeRequest, on_delete=models.CASCADE)
    response = models.CharField(max_length=20, choices=[('approved', 'Approuvé'), ('rejected', 'Rejeté')])
    comments = models.TextField(blank=True)




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=[('employe', 'Employé'), ('chef', 'Chef')])
    chef = models.ForeignKey(User, related_name='employes', on_delete=models.SET_NULL, blank=True, null=True)

from .signals import *