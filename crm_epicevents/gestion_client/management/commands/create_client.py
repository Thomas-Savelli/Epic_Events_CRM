from django.core.management.base import BaseCommand
from gestion_client.models import Client, User
from django.utils import timezone
from gestion_client.permissions import require_login, require_team_commercial, get_user_id_from_token


class Command(BaseCommand):
    help = 'Crée un nouveau client'

    def add_arguments(self, parser):
        parser.add_argument('nom_complet', type=str, help='Nom complet du client')
        parser.add_argument('email', type=str, help='Email du client')
        parser.add_argument('telephone', type=str, help='Numéro de téléphone du client')
        parser.add_argument('entreprise', type=str, help='Entreprise du client')
        parser.add_argument('--date_derniere_maj', type=str,
                            help='Date de dernière mise à jour (format YYYY-MM-DD HH:MM:SS)', required=False)

    @require_login
    @require_team_commercial
    def handle(self, *args, **kwargs):
        nom_complet = kwargs['nom_complet']
        email = kwargs['email']
        telephone = kwargs['telephone']
        entreprise = kwargs['entreprise']
        date_creation = timezone.now()
        date_derniere_maj = kwargs.get('date_derniere_maj')

        commercial_id = get_user_id_from_token()
        try:
            commercial = User.objects.get(id=commercial_id)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Le collaborateur avec l'ID {commercial_id} n'existe pas."))
            return

        client = Client.objects.create(nom_complet=nom_complet, email=email, telephone=telephone,
                                       entreprise=entreprise, date_creation=date_creation,
                                       date_derniere_maj=date_derniere_maj, commercial=commercial)

        self.stdout.write(self.style.SUCCESS(f"Client '{nom_complet}' créé avec succès. ID du client : {client.id}"))
