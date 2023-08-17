# Creation de la vue des demandes 
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, DemandeCongeForm
from .models import CongeRequest
from .models import ChefResponse

def liste(request):
    congerequests = CongeRequest.objects.all()
    # vérifier si vous avez un compte
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #vérifie si vous etes authentifier
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Vous avez été connecté")
            return redirect('liste')
        else:
            messages.success(request, "une erreur s'est produite lors de la connexion, veuillez réessayer...")
            return redirect('liste')
    else:
        return render(request, 'liste.html', {'congerequests':congerequests})
    

def chef(request):
    chefresponses = ChefResponse.objects.all()
    # vérifier si vous avez un compte
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #vérifie si vous etes authentifier
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Vous avez été connecté")
            return redirect('chef')
        else:
            messages.success(request, "une erreur s'est produite lors de la connexion, veuillez réessayer...")
            return redirect('chef')
    else:
        return render(request, 'chef.html', {'chefresponses':chefresponses})



def logout_user(request):
    logout(request)
    messages.success(request, " vous avez été déconnecté... ")
    return redirect('liste')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #s'authentifier et se connecter
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "inscription valider bienvenue!")
            return redirect('liste')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})
    return render(request, 'register.html', {'form':form})





def demande_conge(request):
    form = DemandeCongeForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
               demande_conge = form.save(commit=False)
               demande_conge.user = request.user
               demande_conge.save()
               messages.success(request, "Demander effectuer!")
               return redirect('liste')
        return render(request, 'demande_conge.html', {'form':form})
    else:
        messages.success(request, "Vous devez être connecté!")
        return redirect('liste')