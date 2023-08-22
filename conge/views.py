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
from django.contrib.auth.decorators import login_required




def liste(request):
    congerequests = CongeRequest.objects.all()
    #vérifier si vous avez un compte
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


    


###


'''@login_required
def liste_demandes_conge(request):
    if request.user.userprofile.statut == 'chef':
        employes = UserProfile.objects.filter(chef=request.user)
        congerequests = CongeRequest.objects.filter(user__in=[emp.user for emp in employes])
    else:
        congerequests = CongeRequest.objects.filter(user=request.user)

    return render(request, 'liste_demandes_conge.html', {'congerequests': congerequests})  '''
    

###

@login_required
def liste_demandes_conge(request):
    if request.user.userprofile.statut == 'chef':
        employes = UserProfile.objects.filter(chef=request.user)
        congerequests = CongeRequest.objects.filter(user__in=[emp.user for emp in employes])
    else:
        congerequests = CongeRequest.objects.filter(user=request.user)

    return render(request, 'liste_demandes_conge.html', {'congerequests': congerequests})




        



###

    

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
    return redirect('chef')

##ok



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

            # Si le statut est "chef", associez l'employé choisi au chef
           # if statut == 'chef':
               # employe_associated = form.cleaned_data['employe_associated']
               # if employe_associated:
                #    employe_associated_profile = employe_associated.userprofile
                 #   employe_associated_profile.chef = user
               #     employe_associated_profile.save()

            # Authentification et connexion automatiques
            user = authenticate(username=user.username, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)

            messages.success(request, "Inscription validée, bienvenue!")
            return redirect('liste')  

    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})

##ok
def demande_conge(request):
    form = DemandeCongeForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
               demande_conge = form.save(commit=False)
               demande_conge.user = request.user
               demande_conge.save()
               messages.success(request, "Demander effectuer!")
               return redirect('liste_demandes_conge')
        return render(request, 'demande_conge.html', {'form':form})
    else:
        messages.success(request, "Vous devez être connecté!")
        return redirect('liste_demandes_conge')
    



def valider_demande(request, demande_id):
    demande = get_object_or_404(CongeRequest, id=demande_id)
    
    if request.user.is_authenticated and request.user.userprofile.statut == 'chef' and request.user == demande.user.userprofile.chef:
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
        messages.success(request, "Vous devez avoir le profil chef!")
        return redirect('liste')
    
###


'''def association(request):
    if request.method == 'POST':
        chef_id = request.POST.get('chef')
        employe_id = request.POST.get('employe')

        chef = UserProfile.objects.get(pk=chef_id)
        employe = UserProfile.objects.get(pk=employe_id)

        employe.chef = chef.user
        employe.save()

        return redirect('liste')  

    chefs = UserProfile.objects.filter(statut='chef')
    employes = UserProfile.objects.filter(statut='employe')

    return render(request, 'association.html', {'chefs': chefs, 'employes': employes})'''

    
    #####
from django.contrib import messages

def association(request):
    if request.method == 'POST':
        chef_id = request.POST.get('chef')
        employe_id = request.POST.get('employe')

        chef = UserProfile.objects.get(pk=chef_id)
        employe = UserProfile.objects.get(pk=employe_id)

        # Vérifiez si l'employé a déjà un chef
        if employe.chef is None:
            employe.chef = chef.user
            employe.save()
            messages.success(request, f"L'association de {employe.user.username} avec {chef.user.username} a été effectuée avec succès.")
        else:
            messages.error(request, f"{employe.user.username} a déjà un chef!")

        return redirect('association')

    chefs = UserProfile.objects.filter(statut='chef')
    employes = UserProfile.objects.filter(statut='employe')

    return render(request, 'association.html', {'chefs': chefs, 'employes': employes})


   

