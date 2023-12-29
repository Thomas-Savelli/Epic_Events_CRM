from django.core.management.base import BaseCommand
from gestion_client.models import Evenement
from tabulate import tabulate


class Command(BaseCommand):
    help = 'Affiche les détails des événements'

    def add_arguments(self, parser):
        parser.add_argument('evenement_id', type=int, nargs='?', help='ID de l\'événement à afficher')

    def handle(self, *args, **kwargs):
        evenement_id = kwargs.get('evenement_id')

        if evenement_id is not None:
            try:
                evenement = Evenement.objects.get(pk=evenement_id)
                self.print_evenement_details([evenement])
            except Evenement.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Aucun événement trouvé avec l'ID {evenement_id}."))
        else:
            evenements = Evenement.objects.all()
            if evenements.exists():
                self.print_evenement_details(evenements)
            else:
                self.stdout.write(self.style.SUCCESS("Aucun événement trouvé."))

    def print_evenement_details(self, evenements):
        headers = ["ID", "Contrat", "Nom", "Date de début", "Date de fin", "Support",
                   "Lieu", "Nombre de participants", "Notes"]
        rows = []

        for evenement in evenements:
            row = [
                evenement.id,
                evenement.contrat,
                evenement.nom,
                evenement.date_debut,
                evenement.date_fin,
                evenement.support,
                evenement.lieu,
                evenement.nombre_participants,
                evenement.notes
            ]
            rows.append(row)

        title = "Listes des Événements"
        table = tabulate(rows, headers=headers, tablefmt="pretty")

        # Utilisation d'une chaîne de format traditionnelle
        table_with_title = "{}\n{}".format(title.center(len(table.split('\n')[0])), table)
        print(table_with_title)
