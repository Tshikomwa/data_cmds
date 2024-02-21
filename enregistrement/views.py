# enregistrement/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ExploitantForm
from .models import Exploitant
import qrcode
from io import BytesIO
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Exploitant
from django.shortcuts import render, redirect
from .forms import ExploitantForm
from .models import Exploitant
from django.utils import timezone
from django.http import HttpResponse
from django.forms import modelform_factory
from django.utils import timezone  # Importez le module timezone
from django.http import HttpResponse
from PIL import Image
from io import BytesIO
from enregistrement.models import Exploitant
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


# Page d'acceuil

def accueil(request):
    return render(request, 'enregistrement/accueil.html')

# Fonction pour générer le code QR
# Vue pour gérer l'enregistrement des instances Exploitant

def generate_qrcode(exploitant, size=200):
        
        detail_url = f"http://templates/enregistrement/detail_exploitant/{exploitant.pk}/"
        content = detail_url
        qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        qr.add_data(content)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((size, size))

        # Convert the image to bytes and create an InMemoryUploadedFile
        image_stream = BytesIO()
        img.save(image_stream, format='PNG')
        image_file = InMemoryUploadedFile(
            image_stream,
            None,
            f'qrcode_{exploitant.pk}.png',
            'image/png',
            image_stream.tell(),
            None
        )

        return image_file

def get_qrcode(request, pk):
    exploitant = get_object_or_404(Exploitant, pk=pk)
    img = generate_qrcode(exploitant)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


# views.py
# Vue pour gérer l'enregistrement des instances Exploitant

def recording(request):
    enregistrement_reussi = False
    echec_enregistrement = False

    if request.method == 'POST':
        form = ExploitantForm(request.POST, request.FILES)
        if form.is_valid():
            exploiteur = form.save(commit=False)
            
            # Remplissez les champs date_enregistrement et date_mise_a_jour
            exploiteur.date_enregistrement = timezone.now()
            exploiteur.date_mise_a_jour = timezone.now()
            qr_code = generate_qrcode(exploiteur)
            exploiteur.qrcode = qr_code
            # Enregistrez l'instance Exploitant
            exploiteur.save()

            enregistrement_reussi = True
            return redirect('visualisation')
        else:
            echec_enregistrement = True

    else:
        form = ExploitantForm()

    return render(request, 'enregistrement/recording.html', {'form': form, 'enregistrement_reussi': enregistrement_reussi, 'echec_enregistrement': echec_enregistrement})


# Vue pour afficher la liste de toutes les instances Exploitant
from django.db.models import Q

def visualisation(request):
    # Récupérer tous les exploitants
    exploiteurs = Exploitant.objects.all()

    # Calculer le nombre total d'exploitants
    total_exploitants = exploiteurs.count()

    # Récupérer la valeur de recherche depuis la requête GET
    search_query = request.GET.get('search', '')

    # Si une recherche est effectuée
    if search_query:
        try:
            # Essayez de convertir la recherche en un entier
            search_query_int = int(search_query)

            # Ajoutez une vérification pour ignorer la recherche si elle est un chiffre
            if str(search_query_int) == search_query:
                raise ValueError

            # Filtrez les exploitants en fonction des critères de recherche, y compris le numéro d'ordre
            exploiteurs = exploiteurs.filter(
                Q(nom__icontains=search_query) |
                Q(post_nom__icontains=search_query) |
                Q(prenom__icontains=search_query) |
                Q(numero_ordre=search_query_int)
            )
        except ValueError:
            # La recherche n'est pas un entier, filtrez uniquement par nom, post_nom et prenom
            exploiteurs = exploiteurs.filter(
                Q(nom__icontains=search_query) |
                Q(post_nom__icontains=search_query) |
                Q(prenom__icontains=search_query)
            )

    # Passer les données dans le contexte du rendu du template
    context = {
        'exploiteurs': exploiteurs,
        'total_exploitants': total_exploitants,
        'search_query': search_query,
    }

    return render(request, 'enregistrement/visualisation.html', context)



# Vue pour supprimer un exploitant
def delete_exploitant(request, exploitant_id):
    exploiteur = get_object_or_404(Exploitant, id=exploitant_id)

    if request.method == 'POST':
        exploiteur.delete()
        return redirect('visualisation')

    return render(request, 'enregistrement/delete_exploitant.html', {'exploiteur': exploiteur})

# Vue pour mettre à jour un exploitant
# importez les éléments nécessaires
import os
from django.conf import settings

from django.shortcuts import render, get_object_or_404, redirect
from django.forms.models import modelform_factory
from django.utils import timezone

def update_exploitant(request, exploitant_id):
    exploiteur = get_object_or_404(Exploitant, id=exploitant_id)

    ExploitantForm = modelform_factory(Exploitant, exclude=['qrcode', 'date_enregistrement', 'date_mise_a_jour'])

    modification_reussie = False  # Ajout de la variable de confirmation

    if request.method == 'POST':
        form = ExploitantForm(request.POST, request.FILES, instance=exploiteur)
        if form.is_valid():
            # Mettez à jour la date de mise à jour avant de sauvegarder
            exploiteur.date_mise_a_jour = timezone.now()
            exploiteur.save()

            modification_reussie = True  # Indique que la modification a réussi

            return redirect('visualisation')
    else:
        form = ExploitantForm(instance=exploiteur)

    context = {
        'form': form,
        'exploiteur': exploiteur,
        'modification_reussie': modification_reussie,  # Ajout de la variable au contexte
    }

    return render(request, 'enregistrement/update_exploitant.html', context)



def get_image(request, exploitant_id, field_name):
    exploiteur = Exploitant.objects.get(id=exploitant_id)

    if field_name == 'photo':
        field_data = exploiteur.photo
    elif field_name == 'qrcode':
        field_data = exploiteur.qrcode
    else:
        return HttpResponse("Invalid field name", status=400)

    # Assurez-vous que le champ de l'image est un fichier
    if not field_data:
        return HttpResponse("Image not found", status=404)

    # Ouvrez l'image depuis le chemin du fichier
    image = Image.open(field_data.path)

    # Créez un objet BytesIO pour stocker l'image redimensionnée
    image_bytes = BytesIO()

    # Déterminez le format en fonction de l'extension du fichier
    format_extension = field_data.path.split('.')[-1].lower()
    if format_extension in ['jpeg', 'jpg']:
        image_format = 'JPEG'
    elif format_extension == 'png':
        image_format = 'PNG'
    else:
        return HttpResponse("Unsupported image format", status=400)

    # Sauvegardez l'image redimensionnée dans BytesIO
    image.save(image_bytes, format=image_format)
    image_bytes.seek(0)

    # Créez une réponse avec le contenu de BytesIO et le type de contenu approprié
    response = HttpResponse(image_bytes.read(), content_type=f"image/{image_format.lower()}")
    return response

from django.shortcuts import render, get_object_or_404
from .models import Exploitant  # Replace with your actual model name

def detail_exploitant(request, pk):
    exploitant = get_object_or_404(Exploitant, id=pk)
    return render(request, 'enregistrement/detail_exploitant.html', {'exploitant': exploitant})

# enregistrement/views.py
from django.shortcuts import render, redirect
from .models import Incident
from .forms import IncidentForm  # Supposons que vous ayez un formulaire IncidentForm

from django.shortcuts import render, redirect
from .forms import IncidentForm  # Assuming your form is in a forms.py file in the same directory
import logging

def incident(request):
    if request.method == 'POST':
        logging.debug(request.POST)
        form = IncidentForm(request.POST)
        if form.is_valid():
            # Validate the number of cases
            nombre_cas = form.cleaned_data.get('Nombre_cas')
            if nombre_cas < 1:
                error_message = "Echec d'enregistrement: Le nombre de cas ne peut pas être inférieur à 1"
                return render(request, 'enregistrement/incident.html', {'form': form, 'error_message': error_message})

            # Save the form data
            form.save()
            return redirect('visualiser_incidents')
    else:
        form = IncidentForm()

    return render(request, 'enregistrement/incident.html', {'form': form})


def visual(request):
    incidents = Incident.objects.all()
    return render(request, 'enregistrement/visual.html', {'incidents': incidents})

# Dans votre fichier views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Incident  # Assurez-vous d'importer votre modèle Incident

def delete_incident(request, incident_id):
    # Récupérer l'incident
    incident = get_object_or_404(Incident, id=incident_id)

    if request.method == 'POST':
        # Vérifier la confirmation de suppression
        if request.POST.get('confirmation'):
            # Supprimer l'incident
            incident.delete()
            messages.success(request, 'L\'incident a été supprimé avec succès.')
            return redirect('visualiser_incidents')
        else:
            messages.error(request, 'Veuillez confirmer la suppression pour continuer.')

    return render(request, 'enregistrement/delete_incident.html', {'incident': incident})






