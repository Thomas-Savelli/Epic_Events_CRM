from django.core.management.base import BaseCommand
from gestion_client.models import Client


class Command(BaseCommand):
    help = "Modification d'un client existant"

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int, help='ID du client à modifier')
        parser.add_argument('--nom_complet', type=str, help='Nouveau Nom complet du client', required=False)
        parser.add_argument('--email', type=str, help='Nouvel email du client', required=False)
        parser.add_argument('--telephone', type=str, help='Nouveau numéro de téléphone du client', required=False)
        parser.add_argument('--entreprise', type=str, help='Nouvelle entreprise du client', required=False)

    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']

        try:
            client = Client.objects.get(pk=client_id)

            # Mettez à jour les champs spécifiés
            if kwargs['nom_complet']:
                client.nom_complet = kwargs['nom_complet']
            if kwargs['email']:
                client.email = kwargs['email']
            if kwargs['telephone']:
                client.telephone = kwargs['telephone']
            if kwargs['entreprise']:
                client.entreprise = kwargs['entreprise']

            client.save()
            self.stdout.write(self.style.SUCCESS(f"Le client avec l'ID {client_id} a été modifié avec succès."))
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Le client avec l'ID {client_id} n'existe pas."))
