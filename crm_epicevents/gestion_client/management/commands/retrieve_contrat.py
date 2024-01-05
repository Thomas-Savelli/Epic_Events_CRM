from django.core.management.base import BaseCommand
from tabulate import tabulate
from gestion_client.models import Contrat
from gestion_client.permissions import require_login


class Command(BaseCommand):
    help = 'Affiche les détails d\'un contrat'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, nargs='?', help='ID du contrat à afficher')
        parser.add_argument('--client', type=str, help='Filtre les contrats par client (nom ou ID)', required=False)
        parser.add_argument('--commercial', type=str, help='Filtre les contrats par commercial (nom ou ID)',
                            required=False)
        parser.add_argument('--montant_total', type=float, help='Filtre les contrats par montant total',
                            required=False)
        parser.add_argument('--montant_restant', type=float, help='Filtre les contrats par montant restant',
                            required=False)
        parser.add_argument('--statut', type=str, help='Filtre les contrats par statut', required=False)
        parser.add_argument('--date_creation', type=str,
                            help='Filtre les contrats par date de création (format : YYYY-MM-DD)',
                            required=False)

    @require_login
    def handle(self, *args, **options):
        contrat_id = options['contrat_id']
        client_filter = options['client']
        commercial_filter = options['commercial']
        montant_total_filter = options['montant_total']
        montant_restant_filter = options['montant_restant']
        statut_filter = options['statut']
        date_creation_filter = options['date_creation']

        if contrat_id is not None:
            try:
                contrat = Contrat.objects.get(pk=contrat_id)
                self.print_contrat_details([contrat])
            except Contrat.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Aucun contrat trouvé avec l'ID {contrat_id}."))
        else:
            contrats = Contrat.objects.all()

            if client_filter:
                # essai de filtrage par ID
                try:
                    client_id = int(client_filter)
                    contrats = contrats.filter(client__id=client_id)
                except ValueError:
                    # sinon essai filtrage par nom
                    contrats = contrats.filter(client__nom_complet__icontains=client_filter)

            if commercial_filter:
                # essai de filtrage par ID
                try:
                    commercial_id = int(commercial_filter)
                    contrats = contrats.filter(commercial__id=commercial_id)
                except ValueError:
                    # sinon essai de filtrage par nom
                    contrats = contrats.filter(commercial__nom_complet__icontains=commercial_filter)

            if montant_total_filter:
                contrats = contrats.filter(montant_total=montant_total_filter)

            if montant_restant_filter:
                contrats = contrats.filter(montant_restant=montant_restant_filter)

            if statut_filter:
                contrats = contrats.filter(statut__icontains=statut_filter)

            if date_creation_filter:
                contrats = contrats.filter(date_creation__icontains=date_creation_filter)

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
