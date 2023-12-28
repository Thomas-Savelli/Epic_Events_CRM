from django.core.management.base import BaseCommand, CommandError
from gestion_client.models import User


class Command(BaseCommand):
    help = 'Liste tous les collaborateurs'

    def add_arguments(self, parser):
        parser.add_argument('collaborateur_id', nargs='?', type=int, help='ID du collaborateur à récupérer')

    def handle(self, *args, **options):
        collaborateur_id = options['collaborateur_id']

        if collaborateur_id is not None:
            try:
                collaborateur = User.objects.get(id=collaborateur_id)
                self.stdout.write(self.style.SUCCESS("Informations du collaborateur :"))
                self.stdout.write(f"ID: {collaborateur.id}")
                self.stdout.write(f"Nom complet: {collaborateur.nom_complet}")
                self.stdout.write(f"Nom d'utilisateur: {collaborateur.username}")
                self.stdout.write(f"Rôle: {collaborateur.role}")
            except User.DoesNotExist:
                raise CommandError(f"Collaborateur avec l'ID {collaborateur_id} non trouvé.")
        else:
            collaborateurs = User.objects.all()

            if collaborateurs:
                print("")
                print("Liste des collaborateurs:")
                print("")
                for collaborateur in collaborateurs:
                    print(f"- {collaborateur.id} | {collaborateur.nom_complet} | ({collaborateur.username}) | Rôle: {collaborateur.role}")
                    print("---------------------------------------------------------------------")
            else:
                print("Aucun collaborateur trouvé.")
