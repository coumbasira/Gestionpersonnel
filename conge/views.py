# Creation de la vue des demandes 
from django.shortcuts import render

def liste(request):
    return render(request, 'liste.html', {})
