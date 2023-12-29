from django.core.management.base import BaseCommand, CommandError
from tabulate import tabulate
from gestion_client.models import Client


class Command(BaseCommand):
    help = 'Liste tous les clients'

    def add_arguments(self, parser):
        parser.add_argument('client_id', nargs='?', type=int, help='ID du client à récupérer')

    def handle(self, *args, **options):
        client_id = options['client_id']

        if client_id is not None:
            try:
                client = Client.objects.get(id=client_id)
                self.print_clients_details([client])
            except Client.DoesNotExist:
                raise CommandError(f"Client avec l'ID {client_id} non trouvé.")
        else:
            clients = Client.objects.all()
            if clients:
                self.print_clients_details(clients)
            else:
                self.stdout.write(self.style.SUCCESS("Aucun client trouvé."))

    def print_clients_details(self, data):
        headers = ["ID", "Nom Complet", "Email", "Téléphone", "Entreprise", "Date de Création", "Dernière Mise à Jour"]
        rows = []

        for item in data:
            formatted_date_creation = item.date_creation.strftime('%Y-%m-%d')
            formatted_date_derniere_maj = item.date_derniere_maj.strftime('%Y-%m-%d')
            row = [item.id, item.nom_complet, item.email,
                   item.telephone, item.entreprise,
                   formatted_date_creation, formatted_date_derniere_maj]
            rows.append(row)

        title = "Listes des Clients"
        table = tabulate(rows, headers=headers, tablefmt="pretty")

        # Utilisation d'une chaîne de format traditionnelle
        table_with_title = "{}\n{}".format(title.center(len(table.split('\n')[0])), table)
        print(table_with_title)
