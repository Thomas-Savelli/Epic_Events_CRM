from django.core.management.base import BaseCommand
from gestion_client.models import User


class Command(BaseCommand):
    help = 'Crée un collaborateur avec un nom complet et un rôle'

    def add_arguments(self, parser):
        parser.add_argument('nom_complet', help='Nom complet du collaborateur')
        parser.add_argument('role', help='Rôle du collaborateur (Commercial, Support, Gestion)')
        parser.add_argument('username', help='Nom d\'utilisateur')
        parser.add_argument('password', help='Mot de passe')

    def handle(self, *args, **options):
        nom_complet = options['nom_complet']
        role = options['role']
        username = options['username']
        password = options['password']

        role = role.lower()  # S'assure que le rôle est en minuscules

        # Vérifie que le rôle est parmi les choix valides
        valid_roles = [r[0] for r in User.ROLE_CHOICES]
        if role not in valid_roles:
            self.stdout.write(self.style.ERROR(f"Le rôle '{role}' est invalide. Utilisez l'un des suivants : {', '.join(valid_roles)}"))
            return

        self.stdout.write(self.style.SUCCESS(f"Inputs: {nom_complet}, {role}, {username}, {password}"))

        try:
            user = User.objects.create_user(username=username, password=password, nom_complet=nom_complet, role=role)
            self.stdout.write(self.style.SUCCESS(f"Collaborateur créé avec succès: {user}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur lors de la création du collaborateur: {e}"))
