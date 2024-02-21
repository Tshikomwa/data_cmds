# enregistrement/forms.py
from django import forms
from .models import Exploitant

class ExploitantForm(forms.ModelForm):
    class Meta:
        model = Exploitant
        fields = ['nom', 'post_nom', 'prenom', 'sexe', 'lieu_naissance', 'date_naissance', 'etat_civil', 'nom_conjoint', 'nb_enfants', 'adresse', 'niveau_etude', 'profession', 'fonction', 'telephone', 'photo']
        exclude = ['qrcode', 'date_enregistrement', 'date_mise_a_jour']

    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    post_nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    sexe = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Exploitant.SEXE_CHOICES)
    lieu_naissance = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_naissance = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    etat_civil = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Exploitant.ETAT_CIVIL_CHOICES) 
    nom_conjoint = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    nb_enfants = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    adresse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    niveau_etude = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Exploitant.NIVEAU_ETUDE_CHOICES)
    profession = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    fonction = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), choices=Exploitant.FONCTION_CHOICES)
    telephone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(ExploitantForm, self).__init__(*args, **kwargs)
        # Définissez readonly dans le widget plutôt que dans le champ
        if 'date_enregistrement' in self.fields:
            self.fields['date_enregistrement'].widget.attrs['readonly'] = True
        if 'date_mise_a_jour' in self.fields:
            self.fields['date_mise_a_jour'].widget.attrs['readonly'] = True

    def clean_nb_enfants(self):
        nb_enfants = self.cleaned_data.get('nb_enfants')

        if nb_enfants is not None and nb_enfants < 0:
            raise forms.ValidationError("Le nombre d'enfants ne peut pas être négatif.")

        return nb_enfants
    

# enregistrement/forms.py
from django import forms
from .models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = '__all__'

