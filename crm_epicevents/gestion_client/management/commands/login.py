from django.core.management.base import BaseCommand
from gestion_client.auth_utils import generate_token
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
import getpass


class Command(BaseCommand):
    help = 'Connecte un utilisateur'

    def handle(self, *args, **options):
        # Demander les informations d'identification à l'utilisateur
        username = input("Nom d'utilisateur : ")
        password = getpass.getpass("Mot de passe : ")

        # Authentifier l'utilisateur
        user = authenticate(username=username, password=password)

        if user:
            expiration_time = datetime.utcnow() + timedelta(hours=2)
            token = generate_token(user, expiration_time)

            self.stdout.write(self.style.SUCCESS(f'Connexion réussie! Token généré : {token}'))
        else:
            self.stdout.write(self.style.ERROR('Échec de l\'authentification'))
