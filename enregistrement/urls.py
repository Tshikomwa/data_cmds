from django.urls import path
from .views import accueil, recording, visualisation, delete_exploitant, update_exploitant
from .views import get_image
from .views import detail_exploitant
from .views import incident, visual
from .views import delete_incident


urlpatterns = [
    path('', accueil, name='accueil'),
    path('enregistrement/recording/', recording, name='recording'),
    path('visualisation/', visualisation, name='visualisation'),
    path('delete_exploitant/<int:exploitant_id>/', delete_exploitant, name='delete_exploitant'),
    path('update_exploitant/<int:exploitant_id>/', update_exploitant, name='update_exploitant'),

    # ... autres vues ...

    path('get_image/<int:exploitant_id>/<str:field_name>/', get_image, name='get_image'),
    path('exploitant/<int:pk>/', detail_exploitant, name='detail_exploitant'),
    path('enregistrer-incident/', incident, name='enregistrer_incident'),
    path('visualiser-incidents/', visual, name='visualiser_incidents'),
    path('delete_incident/<int:incident_id>/', delete_incident, name='delete_incident'),
]





