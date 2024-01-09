from django.core.management.base import BaseCommand
from gestion_client.models import User
from gestion_client.permissions import require_login, require_team_gestion


class Command(BaseCommand):
    help = 'Modifie un collaborateur existant'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID du collaborateur à modifier')
        parser.add_argument('--nom_complet', type=str, help='Nouveau nom complet du collaborateur')
        parser.add_argument('--role', type=str, help='Nouveau rôle du collaborateur')
        parser.add_argument('--username', type=str, help='Nouveau nom d\'utilisateur du collaborateur')
        parser.add_argument('--password', type=str, help='Nouveau mot de passe du collaborateur')

    @require_login
    @require_team_gestion
    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        nom_complet = kwargs['nom_complet']
        role = kwargs['role']
        new_username = kwargs['username']
        # password = kwargs['password']

        try:
            collaborateur = User.objects.get(id=user_id)

            if nom_complet:
                collaborateur.nom_complet = nom_complet

            if role:
                collaborateur.role = role

            if new_username:
                collaborateur.username = new_username

            # if password:
            #     collaborateur.set_password(password)

            collaborateur.save()
            self.stdout.write(self.style.SUCCESS(f"Collaborateur avec l'ID {user_id} modifié avec succès"))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Collaborateur avec l'ID {user_id} non trouvé"))
