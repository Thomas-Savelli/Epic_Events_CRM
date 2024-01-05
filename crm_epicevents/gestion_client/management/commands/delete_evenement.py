from django.core.management.base import BaseCommand
from gestion_client.models import Evenement
from gestion_client.permissions import require_login


class Command(BaseCommand):
    help = 'Suppression d\'un événement existant'

    def add_arguments(self, parser):
        parser.add_argument('evenement_id', type=int, help='ID de l\'événement à supprimer')

    @require_login
    def handle(self, *args, **options):
        evenement_id = options['evenement_id']

        try:
            evenement = Evenement.objects.get(pk=evenement_id)
            evenement.delete()
            self.stdout.write(self.style.SUCCESS(f"Événement avec l'ID {evenement_id} supprimé avec succès."))
        except Evenement.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"L'événement avec l'ID {evenement_id} n'existe pas."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Une erreur s'est produite : {e}"))
