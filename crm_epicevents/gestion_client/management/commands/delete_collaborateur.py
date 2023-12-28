from django.core.management.base import BaseCommand
from gestion_client.models import User


class Command(BaseCommand):
    help = 'Supprime un collaborateur existant'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='ID du collaborateur à supprimer')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']

        try:
            collaborateur = User.objects.get(id=user_id)
            collaborateur.delete()
            self.stdout.write(self.style.SUCCESS(f"Collaborateur avec l'ID {user_id} supprimé avec succès"))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Collaborateur avec l'ID {user_id} non trouvé"))
