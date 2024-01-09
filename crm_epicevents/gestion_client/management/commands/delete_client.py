from django.core.management.base import BaseCommand
from gestion_client.models import Client
from gestion_client.permissions import require_login, require_team_commercial_and_client_access


class Command(BaseCommand):
    help = 'Supprime un client existant'

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int, help='ID du client à supprimer')

    @require_login
    @require_team_commercial_and_client_access
    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']

        try:
            client = Client.objects.get(id=client_id)
            client.delete()
            self.stdout.write(self.style.SUCCESS(f"Le Client avec l'ID {client_id} supprimé avec succès"))
        except Client.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Client avec l'ID {client_id} non trouvé"))
