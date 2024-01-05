from django.core.management.base import BaseCommand
from gestion_client.auth_utils import load_token
import os


class Command(BaseCommand):
    help = 'Déconnecte l\'utilisateur en supprimant le token'

    def handle(self, *args, **options):
        # Charger le token depuis le fichier
        token, _ = load_token()

        if token:
            # Supprimer le fichier .token
            os.remove('.token')
            self.stdout.write(self.style.SUCCESS('Déconnexion réussie!'))
        else:
            self.stdout.write(self.style.SUCCESS('Aucun token trouvé. L\'utilisateur n\'est pas connecté.'))
