"""
Middleware personnalisé pour servir les fichiers média en production
"""

import os
from django.conf import settings
from django.http import Http404
from django.views.static import serve


class MediaFilesMiddleware:
    """
    Middleware pour servir les fichiers média en production
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Vérifier si la requête concerne un fichier média
        if request.path.startswith(settings.MEDIA_URL):
            # Construire le chemin complet du fichier
            file_path = request.path.replace(settings.MEDIA_URL, '', 1)
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            # Vérifier si le fichier existe
            if os.path.exists(full_path) and os.path.isfile(full_path):
                # Servir le fichier
                return serve(request, file_path, document_root=settings.MEDIA_ROOT)
            else:
                # Fichier non trouvé
                raise Http404("Fichier média non trouvé")
        
        # Continuer avec la requête normale
        return self.get_response(request)
