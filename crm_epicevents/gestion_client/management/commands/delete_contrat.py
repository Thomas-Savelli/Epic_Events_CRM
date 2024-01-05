from django.core.management.base import BaseCommand
from gestion_client.models import Contrat
from gestion_client.permissions import require_login


class Command(BaseCommand):
    help = 'Suppression d\'un contrat existant'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, help='ID du contrat à supprimer')

    @require_login
    def handle(self, *args, **options):
        contrat_id = options['contrat_id']

        try:
            contrat = Contrat.objects.get(pk=contrat_id)
        except Contrat.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Le contrat avec l'ID {contrat_id} n'existe pas."))
            return

        contrat.delete()

        self.stdout.write(self.style.SUCCESS(f"Contrat avec l'ID {contrat_id} supprimé avec succès."))
