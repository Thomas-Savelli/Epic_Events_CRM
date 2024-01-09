from django.core.management.base import BaseCommand
from gestion_client.models import Contrat, User
from gestion_client.permissions import require_login, require_commercial_contrat_access_or_team_gestion


class Command(BaseCommand):
    help = 'Mise à jour des informations d\'un contrat existant'

    def add_arguments(self, parser):
        parser.add_argument('contrat_id', type=int, help='ID du contrat à mettre à jour')
        parser.add_argument('--montant_total', type=float, help='Nouveau montant total', required=False)
        parser.add_argument('--montant_restant', type=float, help='Nouveau montant restant')
        parser.add_argument('--statut', type=str, help='Nouveau statut')
        parser.add_argument('--commercial_id', type=int, help='ID du nouveau Commercial', required=False)

    @require_login
    @require_commercial_contrat_access_or_team_gestion
    def handle(self, *args, **options):
        contrat_id = options['contrat_id']
        montant_total = options['montant_total']
        montant_restant = options['montant_restant']
        statut = options['statut']
        commercial_id = options['commercial_id']

        try:
            contrat = Contrat.objects.get(pk=contrat_id)
        except Contrat.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Le contrat avec l'ID {contrat_id} n'existe pas."))
            return

        if commercial_id is not None:
            try:
                collaborateur_commercial = User.objects.get(pk=commercial_id, role='commercial')
                contrat.commercial = collaborateur_commercial
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR("Le collaborateur commercial avec l'ID spécifié n'existe pas ou n'est pas un commercial."))
                return

        if montant_total is not None:
            contrat.montant_total = montant_total

        if montant_restant is not None:
            contrat.montant_restant = montant_restant

        # Vérifie que le statut est parmi les choix valides
        if statut is not None:
            valid_statuts = [choice[0] for choice in Contrat.STATUT_CHOICES]
            if statut not in valid_statuts:
                self.stdout.write(self.style.ERROR(f"Le statut '{statut}' est invalide. Utilisez l'un des suivants : {', '.join(valid_statuts)}"))
                return
            contrat.statut = statut

        contrat.save()

        self.stdout.write(self.style.SUCCESS(f"Contrat avec l'ID {contrat_id} mis à jour avec succès."))
