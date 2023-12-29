from django.core.management.base import BaseCommand
from tabulate import tabulate
from gestion_client.models import Contrat


class Command(BaseCommand):
    help = 'Affiche les détails d\'un contrat en fonction de son ID ou tous les contrats'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, nargs='?', help='ID du contrat à afficher')

    def handle(self, *args, **kwargs):
        contrat_id = kwargs.get('contrat_id')

        if contrat_id is not None:
            try:
                contrat = Contrat.objects.get(pk=contrat_id)
                self.print_contrat_details([contrat])
            except Contrat.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Aucun contrat trouvé avec l'ID {contrat_id}."))
        else:
            contrats = Contrat.objects.all()
            if contrats.exists():
                self.print_contrat_details(contrats)
            else:
                self.stdout.write(self.style.SUCCESS("Aucun contrat trouvé."))

    def print_contrat_details(self, contrats):
        headers = ["ID", "Client", "Commercial", "Montant total", "Montant restant", "Statut", "Date de création"]
        rows = []

        for contrat in contrats:
            row = [contrat.id, contrat.client, contrat.commercial, contrat.montant_total,
                   contrat.montant_restant, contrat.get_statut_display(), contrat.date_creation]
            rows.append(row)

        title = "Listes des Contrats"
        table = tabulate(rows, headers=headers, tablefmt="pretty")

        # Utilisation d'une chaîne de format traditionnelle
        table_with_title = "{}\n{}".format(title.center(len(table.split('\n')[0])), table)
        print(table_with_title)
