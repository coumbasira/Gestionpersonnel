#from typing import Any
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import CongeRequest
from .models import ChefResponse
from .models import UserProfile
from django.contrib.admin.widgets import AdminDateWidget

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    statut = forms.ChoiceField(choices=[('employe', 'Employé'), ('chef', 'Chef')])

    employe_associated = forms.ModelChoiceField(queryset=UserProfile.objects.filter(statut='employe'), required=False)


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class']='form-control'
        self.fields['username'].widget.attrs['placeholder']='User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_only.</small></span>'


        self.fields['password1'].widget.attrs['class']='form-control'
        self.fields['password1'].widget.attrs['placeholder']='password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class= "form-text text-muted small"><li>your password can\'t be too similar to your other personal information.</li><li>your password must contain at least 8 characters.</li><li> your password can\'t be a commonly used password.</li><li>your password can\'t be entirely numeric.</li></lu>'


        self.fields['password2'].widget.attrs['class']='form-control'
        self.fields['password2'].widget.attrs['placeholder']='confirm password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verication.</small></span>'

class SignUpForm(UserCreationForm):
    # ... ajout du champs chef dans le formulaire

    statut = forms.ChoiceField(choices=[('employe', 'Employé'), ('chef', 'Chef')])

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'statut')
        

class DemandeCongeForm(forms.ModelForm):
    class Meta:
        model = CongeRequest
        fields = ['motif', 'date_depart', 'date_arrivee']
        widgets = {
            'date_depart': forms.DateInput(attrs={'type': 'date'}),
            'date_arrivee': forms.DateInput(attrs={'type': 'date'}),
        }

       

class ChefResponseForm(forms.ModelForm):
    class Meta:
        model = ChefResponse
        fields = ['response', 'comments']