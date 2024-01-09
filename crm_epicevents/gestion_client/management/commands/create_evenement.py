from django.core.management.base import BaseCommand, CommandError
from gestion_client.models import Evenement, Contrat, User
from datetime import datetime
from gestion_client.permissions import require_login, require_commercial_event_access


class Command(BaseCommand):
    help = 'Crée un nouvel événement'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, help='ID du contrat lié à l\'événement')
        parser.add_argument('nom', type=str, help='Nom de l\'événement')
        parser.add_argument('date_debut', type=str, help='Date de début de l\'événement (au format YYYYMMDD)')
        parser.add_argument('date_fin', type=str, help='Date de fin de l\'événement (au format YYYYMMDD)')
        parser.add_argument('support_id', type=int, help='ID du collaborateur (support)')
        parser.add_argument('lieu', type=str, help='Lieu de l\'événement')
        parser.add_argument('nombre_participants', type=int, help='Nombre de participants')
        parser.add_argument('notes', type=str, help='Notes sur l\'événement')

    @require_login
    @require_commercial_event_access
    def handle(self, *args, **options):
        contrat_id = options['contrat_id']
        nom = options['nom']
        date_debut = options['date_debut']
        date_fin = options['date_fin']
        support_id = options['support_id']
        lieu = options['lieu']
        nombre_participants = options['nombre_participants']
        notes = options['notes']

        # Vérification que le contrat existe
        try:
            contrat = Contrat.objects.get(pk=contrat_id)
        except Contrat.DoesNotExist:
            raise CommandError(f"Le contrat avec l'ID {contrat_id} n'existe pas.")

        # Vérification que le collaborateur de support existe et a le rôle "Support"
        try:
            support = User.objects.get(pk=support_id, role='support')
        except User.DoesNotExist:
            raise CommandError(f"Le collaborateur support avec l'ID {support_id} n'existe pas ou n'est pas de rôle 'Support'.")

        # Conversion des dates de début et de fin
        try:
            date_debut = datetime.strptime(options['date_debut'], '%Y%m%d').date()
            date_fin = datetime.strptime(options['date_fin'], '%Y%m%d').date()
        except ValueError:
            self.stdout.write(self.style.ERROR("Format de date invalide. Utilisez le format YYYYMMDD."))
            return

        # Création de l'événement
        evenement = Evenement.objects.create(
            contrat=contrat,
            nom=nom,
            date_debut=date_debut,
            date_fin=date_fin,
            support=support,
            lieu=lieu,
            nombre_participants=nombre_participants,
            notes=notes
        )

        self.stdout.write(self.style.SUCCESS(f"Événement créé avec succès: {evenement}"))
