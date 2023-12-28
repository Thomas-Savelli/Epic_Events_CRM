from django.core.management.base import BaseCommand, CommandError
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
                formatted_date_creation = client.date_creation.strftime('%Y-%m-%d')
                formatted_date_derniere_maj = client.date_derniere_maj.strftime('%Y-%m-%d')
                self.stdout.write(self.style.SUCCESS("Informations du client :"))
                self.stdout.write(f"ID: {client.id}")
                self.stdout.write(f"Nom complet: {client.nom_complet}")
                self.stdout.write(f"Email: {client.email}")
                self.stdout.write(f"Telephone: {client.telephone}")
                self.stdout.write(f"Entreprise: {client.entreprise}")
                self.stdout.write(f"Création fiche: {formatted_date_creation}")
                self.stdout.write(f"Date dernier contact: {formatted_date_derniere_maj}")
            except Client.DoesNotExist:
                raise CommandError(f"Client avec l'ID {client_id} non trouvé.")
        else:
            clients = Client.objects.all()
            if clients:
                print("")
                print("Liste des clients:")
                print("")
                for client in clients:
                    print(f"- {client.id} | {client.nom_complet} | {client.email} | {client.telephone} | {client.entreprise}")
                    print("---------------------------------------------------------------------")
            else:
                print("Aucun client trouvé.")
