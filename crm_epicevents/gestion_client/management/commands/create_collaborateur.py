from django.core.management.base import BaseCommand
import getpass
from gestion_client.models import User
from gestion_client.permissions import require_login, require_team_gestion


class Command(BaseCommand):
    help = 'Crée un collaborateur avec un nom complet et un rôle'

    def add_arguments(self, parser):
        parser.add_argument('nom_complet', help='Nom complet du collaborateur')
        parser.add_argument('role', help='Rôle du collaborateur (Commercial, Support, Gestion)')
        parser.add_argument('username', help='Nom d\'utilisateur')

    @require_login
    @require_team_gestion
    def handle(self, *args, **options):
        nom_complet = options['nom_complet']
        role = options['role']
        username = options['username']
        password = getpass.getpass('password')

        role = role.lower()  # S'assure que le rôle est en minuscules

        # Vérifie que le rôle est parmi les choix valides
        valid_roles = [r[0] for r in User.ROLE_CHOICES]
        if role not in valid_roles:
            self.stdout.write(self.style.ERROR(f"Le rôle '{role}' est invalide. Utilisez l'un des suivants : {', '.join(valid_roles)}"))
            return

        self.stdout.write(self.style.SUCCESS(f"Inputs: {nom_complet}, {role}, {username}"))

        user = User.objects.create_user(username=username, password=password,
                                        nom_complet=nom_complet, role=role)
        self.stdout.write(self.style.SUCCESS(f"Collaborateur créé avec succès: {user}"))
