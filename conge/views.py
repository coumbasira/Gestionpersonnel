# Creation de la vue des demandes 
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, DemandeCongeForm
from .models import CongeRequest, ChefResponse
from .forms import ChefResponseForm
from .models import UserProfile
from django.shortcuts import render, get_object_or_404

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

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            statut = form.cleaned_data['statut']
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.statut = statut
            profile.save()

            # Effectuez d'autres actions si nécessaires, comme la redirection vers une autre page
            return redirect('liste')  
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})


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
    



def valider_demande(request, demande_id):
    demande = get_object_or_404(CongeRequest, id=demande_id)
    
    if request.user.is_authenticated and request.user.userprofile.statut == 'chef':
        if request.method == 'POST':
            form = ChefResponseForm(request.POST)
            if form.is_valid():
                response = form.save(commit=False)
                response.request = demande
                response.save()
                # Mettre à jour le statut de la demande en fonction de la réponse (approuvé ou rejeté)
                if response.response == 'approved':
                    demande.status = 'approved'
                else:
                    demande.status = 'rejected'
                demande.save()
                return redirect('liste')  
        else:
            form = ChefResponseForm()
        return render(request, 'valider_demande.html', {'form': form, 'demande': demande})
    else:
        messages.success(request, "Vous devez être chef!")
        return redirect('liste')
