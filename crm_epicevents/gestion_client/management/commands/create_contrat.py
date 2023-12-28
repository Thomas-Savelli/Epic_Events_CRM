from django.core.management.base import BaseCommand
from gestion_client.models import Contrat, User, Client


class Command(BaseCommand):
    help = 'Crée un nouveau contrat'

    def add_arguments(self, parser):
        parser.add_argument('client_id', type=int, help='ID du client associé au contrat')
        parser.add_argument('commercial_id', type=int, help='ID du commercial associé au contrat')
        parser.add_argument('montant_total', type=float, help='Montant total du contrat')
        parser.add_argument('montant_restant', type=float, help='Montant restant à payer du contrat')
        parser.add_argument('statut', type=str, help='Statut du contrat')

    def handle(self, *args, **kwargs):
        client_id = kwargs['client_id']
        commercial_id = kwargs['commercial_id']
        montant_total = kwargs['montant_total']
        montant_restant = kwargs['montant_restant']
        statut = kwargs['statut'].lower()  # Converti le statut en minuscules pour éviter les problèmes de casse

        # Vérifie si le statut fourni est parmi les choix valides
        valid_statuts = [choice[0].lower() for choice in Contrat.STATUT_CHOICES]
        if statut not in valid_statuts:
            self.stdout.write(self.style.ERROR(f"Le statut '{statut}' est invalide. Choisissez parmi les options suivantes: {', '.join(valid_statuts)}"))
            return

        # Vérifier si les IDs de client et commercial existent
        try:
            client = Client.objects.get(pk=client_id)
        except Client.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Aucun client trouvé avec l'ID {client_id}."))
            return

        try:
            commercial = User.objects.get(pk=commercial_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Aucun commercial trouvé avec l'ID {commercial_id}."))
            return

        # Vérifier si le rôle du collaborateur est commercial
        if commercial.role.lower() != 'commercial':
            self.stdout.write(self.style.ERROR(f"Le collaborateur avec l'ID {commercial_id} n'a pas le rôle 'commercial'."))
            return

        contrat = Contrat.objects.create(
            client=client,
            commercial=commercial,
            montant_total=montant_total,
            montant_restant=montant_restant,
            statut=statut
        )

        self.stdout.write(self.style.SUCCESS(f"Contrat {contrat.id} créé avec succès."))
