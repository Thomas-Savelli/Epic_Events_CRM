import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from gestion_client.management.commands.create_evenement import Command
from gestion_client.models import Contrat, User, Client
from datetime import datetime, timedelta
from unittest.mock import patch, Mock


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_create_evenements_success(mocker, custom_input):
    # Créer un client fictif pour le test
    client = Client.objects.create(nom_complet='Client Test', email='test@example.com')

    # Créer un commercial fictif pour le test
    commercial = User.objects.create_user(username='testcommercial',
                                          password='testpassword', nom_complet='Test Commercial', role='commercial')

    # Créer un contrat fictif pour le test
    contrat = Contrat.objects.create(client=client, commercial=commercial, montant_total='1000.00',
                                     montant_restant='800.00', statut='En cours')

    # Créer un support fictif pour le test
    support_user = User.objects.create(username='testsupport', role='support')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='commercial')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=support_user)

        # Capture de la sortie standard pour vérification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Création d'une instance de la commande
            call_command('create_evenement', str(contrat.id), 'Nom Evenement', '20220101', '20220105',
                         str(support_user.id), 'Lieu Evenement', 50, 'Notes Evenement')

            # Vérification du message de succès
            assert "Événement créé avec succès" in mock_stdout.write.call_args[0][0]


@pytest.mark.django_db
def test_create_evenements_permission_failure(mocker, custom_input):
    # Créer un client fictif pour le test
    client = Client.objects.create(nom_complet='Client Test', email='test@example.com')

    # Créer un utilisateur fictif pour le test (rôle: 'commercial' plutôt que 'support')
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='commercial')

    # Créer un contrat fictif pour le test
    contrat = Contrat.objects.create(client=client, commercial=user, montant_total='1000.00',
                                     montant_restant='800.00', statut='En cours')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation (rôle: 'gestion' plutôt que 'commercial')
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='gestion')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=user)

        # Capture de la sortie standard pour vérification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Création d'une instance de la commande
            cmd = Command()

            # Appel de la fonction handle de la commande avec les arguments corrects
            try:
                cmd.handle(contrat_id=str(contrat.id), nom='Nom Evenement', date_debut='20220101', date_fin='20220105',
                           support_id='1', lieu='Lieu Evenement', nombre_participants=50, notes='Notes Evenement')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == "Vous n'avez pas la permission d'effectuer cette action."


@pytest.mark.django_db
def test_create_evenements_unauthenticated_user(mocker, custom_input):
    # Créer un client fictif pour le test
    client = Client.objects.create(nom_complet='Client Test', email='test@example.com')

    # Créer un utilisateur fictif pour le test (rôle: 'commercial' plutôt que 'support')
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='commercial')

    # Créer un contrat fictif pour le test
    contrat = Contrat.objects.create(client=client, commercial=user, montant_total='1000.00',
                                     montant_restant='800.00', statut='En cours')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation (utilisateur non connecté)
        mocker.patch('gestion_client.permissions.load_token', return_value=None)

        # Capture de la sortie standard pour vérification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Création d'une instance de la commande
            cmd = Command()

            # Appel de la fonction handle de la commande avec les arguments corrects
            try:
                cmd.handle(contrat_id=str(contrat.id), nom='Nom Evenement', date_debut='20220101', date_fin='20220105',
                           support_id='1', lieu='Lieu Evenement', nombre_participants=50, notes='Notes Evenement')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == "L'utilisateur n'est pas connecté. Veuillez vous connecter."
