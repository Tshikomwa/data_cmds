# enregistrement/models.py
from django.db import models
from django.utils import timezone


class Exploitant(models.Model):

    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]

    ETAT_CIVIL_CHOICES = [
        ('C', 'Célibataire'),
        ('M', 'Marié(e)'),
        ('D', 'Divorcé(e)'),
        ('V', 'Veuf/Veuve'),
    ]

    NIVEAU_ETUDE_CHOICES = [
        ('Aucun', 'Aucun'),
        ('Primaire', 'Primaire'),
        ('Secondaire', 'Secondaire'),
        ('Diplômé(e) d\'Etat', 'Diplômé(e) d\'Etat'),
        ('Gradué(e)', 'Gradué(e)'),
        ('Licencié(e)', 'Licencié(e)'),
        ('Ingénieur(e)', 'Ingénieur(e)'),
        ('Docteur', 'Docteur'),
        ('Autre', 'Autre'),
    ]

    FONCTION_CHOICES = [
        ('Creuseur', 'Creuseur'),
        ('Constructeur', 'Constructeur'),
        ('Agent Mobile', 'Agent Mobile'),
        ('Agent de Sécurité', 'Agent de Sécurité'),
        ('Membre du Comité', 'Membre du Comité'),
        ('Membre de la Coopérative', 'Membre de la Coopérative'),
        ('Laveuse', 'Laveuse'),
        ('Négociant', 'Négociant'),
        ('Sponsor', 'Sponsor'),
        ('Cleaner', 'Cleaner'),
        ('Agent de Bureau', 'Agent de Bureau'),
    ]

    nom = models.CharField(max_length=255)
    post_nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES)
    lieu_naissance = models.CharField(max_length=255)
    date_naissance = models.DateField()
    etat_civil = models.CharField(max_length=20, choices=ETAT_CIVIL_CHOICES)
    nom_conjoint = models.CharField(max_length=255, blank=True, null=True)
    nb_enfants = models.PositiveIntegerField(default=0)
    adresse = models.CharField(max_length=500)
    niveau_etude = models.CharField(max_length=50, choices=NIVEAU_ETUDE_CHOICES)
    profession = models.CharField(max_length=255)
    fonction = models.CharField(max_length=255, choices=FONCTION_CHOICES)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    date_enregistrement = models.DateTimeField(default=timezone.now, editable=False)
    date_mise_a_jour = models.DateTimeField(default=timezone.now, editable=False)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    qrcode = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.nom} {self.post_nom} {self.prenom}"

# enregistrement/models.py
from django.db import models
from django.utils import timezone

class Incident(models.Model):

    CHOICES1 = [
        ('Mortel', 'Mortel'),
        ('Non-mortel', 'Non-mortel'),
    ]

    date_incident = models.DateTimeField(default=timezone.now)
    lieu = models.CharField(max_length=500)
    type_incident = models.CharField(max_length=500, choices=CHOICES1)
    Nombre_cas = models.IntegerField()  # Changer le champ en IntegerField pour les informations en nombre/chiffre
    Noms_accidentes = models.CharField(max_length=500)
    cause_incident = models.CharField(max_length=500)
    Description = models.CharField(max_length=500)
    rapporteur = models.CharField(max_length=500)
    proprietaire = models.CharField(max_length=500)
    actions = models.CharField(max_length=1000)

    def __str__(self):
        return f"Incident le {self.date_incident}"


