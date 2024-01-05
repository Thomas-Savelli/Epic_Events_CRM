from django.core.management.base import BaseCommand
from gestion_client.models import Evenement, User
from datetime import datetime
from gestion_client.permissions import require_login


class Command(BaseCommand):
    help = 'Mise à jour des informations d\'un événement existant'

    def add_arguments(self, parser):
        parser.add_argument('evenement_id', type=int, help='ID de l\'événement à mettre à jour')
        parser.add_argument('--nom', type=str, help='Nouveau nom', required=False)
        parser.add_argument('--date_debut', type=str, help='Nouvelle date de début (format YYYYMMDD)', required=False)
        parser.add_argument('--date_fin', type=str, help='Nouvelle date de fin (format YYYYMMDD)', required=False)
        parser.add_argument('--lieu', type=str, help='Nouveau lieu', required=False)
        parser.add_argument('--nombre_participants', type=int, help='Nouveau nombre de participants', required=False)
        parser.add_argument('--notes', type=str, help='Nouvelles notes', required=False)
        parser.add_argument('--support_id', type=int, help='ID du nouveau Collaborateur support', required=False)

    @require_login
    def handle(self, *args, **options):
        evenement_id = options['evenement_id']
        nom = options['nom']
        date_debut = options['date_debut']
        date_fin = options['date_fin']
        lieu = options['lieu']
        nombre_participants = options['nombre_participants']
        notes = options['notes']
        support_id = options['support_id']

        try:
            evenement = Evenement.objects.get(pk=evenement_id)
        except Evenement.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"L'événement avec l'ID {evenement_id} n'existe pas."))
            return

        if nom:
            evenement.nom = nom

        if date_debut:
            # Convertir la date en objet datetime
            evenement.date_debut = datetime.strptime(date_debut, '%Y%m%d')

        if date_fin:
            # Convertir la date en objet datetime
            evenement.date_fin = datetime.strptime(date_fin, '%Y%m%d')

        if lieu:
            evenement.lieu = lieu

        if nombre_participants is not None:
            evenement.nombre_participants = nombre_participants

        if notes:
            evenement.notes = notes

        if support_id is not None:
            try:
                support = User.objects.get(pk=support_id, role='support')
                evenement.support = support
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR("Le support avec l'ID spécifié n'existe pas ou n'est pas un support."))
                return

        evenement.save()

        self.stdout.write(self.style.SUCCESS(f"Événement avec l'ID {evenement_id} mis à jour avec succès."))
