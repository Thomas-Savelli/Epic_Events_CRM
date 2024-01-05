from django.core.management.base import BaseCommand, CommandError
from tabulate import tabulate
from gestion_client.models import User
from gestion_client.permissions import require_login


class Command(BaseCommand):
    help = 'Liste tous les collaborateurs'

    def add_arguments(self, parser):
        parser.add_argument('collaborateur_id', nargs='?', type=int, help='ID du collaborateur à récupérer')
        parser.add_argument('--nom_complet', type=str, help='Filtre les collaborateurs par nom complet',
                            required=False)
        parser.add_argument('--username', type=str, help='Filtre les collaborateurs par nom d\'utilisateur',
                            required=False)
        parser.add_argument('--role', type=str, help='Filtre les collaborateurs par rôle', required=False)

    @require_login
    def handle(self, *args, **options):
        collaborateur_id = options['collaborateur_id']
        nom_complet_filter = options['nom_complet']
        username_filter = options['username']
        role_filter = options['role']

        if collaborateur_id is not None:
            try:
                collaborateur = User.objects.get(id=collaborateur_id)
                self.print_collaborateurs_details([collaborateur])
            except User.DoesNotExist:
                raise CommandError(f"Collaborateur avec l'ID {collaborateur_id} non trouvé.")
        else:
            collaborateurs = User.objects.all()

            if nom_complet_filter:
                collaborateurs = collaborateurs.filter(nom_complet__icontains=nom_complet_filter)

            if username_filter:
                collaborateurs = collaborateurs.filter(username__icontains=username_filter)

            if role_filter:
                collaborateurs = collaborateurs.filter(role__icontains=role_filter)

            if collaborateurs:
                self.print_collaborateurs_details(collaborateurs)
            else:
                self.stdout.write(self.style.SUCCESS("Aucun collaborateur trouvé."))

    def print_collaborateurs_details(self, data):
        headers = ["ID", "Nom Complet", "Nom d'Utilisateur", "Rôle"]
        rows = []

        for item in data:
            row = [item.id, item.nom_complet, item.username, item.get_role_display()]
            rows.append(row)

        title = "Listes des Collaborateurs"
        table = tabulate(rows, headers=headers, tablefmt="pretty")

        # Utilisation d'une chaîne de format traditionnelle
        table_with_title = "{}\n{}".format(title.center(len(table.split('\n')[0])), table)
        self.stdout.write(table_with_title)
