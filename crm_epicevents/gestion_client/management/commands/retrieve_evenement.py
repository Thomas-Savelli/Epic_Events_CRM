from django.core.management.base import BaseCommand
from gestion_client.models import Evenement
from tabulate import tabulate
from gestion_client.permissions import require_login


class Command(BaseCommand):
    help = 'Affiche les détails des événements'

    def add_arguments(self, parser):
        parser.add_argument('evenement_id', type=int, nargs='?', help='ID de l\'événement à afficher')
        parser.add_argument('--contrat', type=int, help='Filtre les événements par contrat (ID)', required=False)
        parser.add_argument('--nom', type=str, help='Filtre les événements par nom', required=False)
        parser.add_argument('--date_debut', type=str, help='Filtre les événements par date de début (format : YYYY-MM ou YYYY-MM-DD)',
                            required=False)
        parser.add_argument('--date_fin', type=str, help='Filtre les événements par date de fin (format : YYYY-MM ou YYYY-MM-DD)',
                            required=False)
        parser.add_argument('--support', type=str, help='Filtre les événements par support (nom ou ID)',
                            required=False)
        parser.add_argument('--lieu', type=str, help='Filtre les événements par lieu', required=False)
        parser.add_argument('--participants', type=str, help='Filtre les événements par nombre de participants (ex: -50, +50, +100, +200)',
                            required=False)

    @require_login
    def handle(self, *args, **options):
        evenement_id = options['evenement_id']
        contrat_filter = options['contrat']
        nom_filter = options['nom']
        date_debut_filter = options['date_debut']
        date_fin_filter = options['date_fin']
        support_filter = options['support']
        lieu_filter = options['lieu']
        participants_filter = options['participants']

        if evenement_id is not None:
            try:
                evenement = Evenement.objects.get(pk=evenement_id)
                self.print_evenement_details([evenement])
            except Evenement.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Aucun événement trouvé avec l'ID {evenement_id}."))
        else:
            evenements = Evenement.objects.all()

            if contrat_filter:
                evenements = evenements.filter(contrat__id=contrat_filter)

            if nom_filter:
                evenements = evenements.filter(nom__icontains=nom_filter)

            if date_debut_filter:
                evenements = evenements.filter(date_debut__icontains=date_debut_filter)

            if date_fin_filter:
                evenements = evenements.filter(date_fin__icontains=date_fin_filter)

            if support_filter:
                # essai de filtrage par ID
                try:
                    support_id = int(support_filter)
                    evenements = evenements.filter(support__id=support_id)
                except ValueError:
                    # essai de filtrage par nom
                    evenements = evenements.filter(support__nom_complet__icontains=support_filter)

            if lieu_filter:
                evenements = evenements.filter(lieu__icontains=lieu_filter)

            if participants_filter:
                # Gestion des filtres par nombre de participants
                if participants_filter == '-50':
                    evenements = evenements.filter(nombre_participants__lt=50)
                elif participants_filter == '+50':
                    evenements = evenements.filter(nombre_participants__gte=50)
                elif participants_filter == '+100':
                    evenements = evenements.filter(nombre_participants__gte=100)
                elif participants_filter == '+200':
                    evenements = evenements.filter(nombre_participants__gte=200)

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
