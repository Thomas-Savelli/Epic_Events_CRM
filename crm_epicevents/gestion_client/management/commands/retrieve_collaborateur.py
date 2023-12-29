from django.core.management.base import BaseCommand, CommandError
from tabulate import tabulate
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
                self.print_collaborateurs_details([collaborateur])
            except User.DoesNotExist:
                raise CommandError(f"Collaborateur avec l'ID {collaborateur_id} non trouvé.")
        else:
            collaborateurs = User.objects.all()
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
        print(table_with_title)
