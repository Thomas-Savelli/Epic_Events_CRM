import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from gestion_client.models import Contrat, User, Client
from datetime import datetime, timedelta
from unittest.mock import patch, Mock


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_delete_contrat_success(mocker, custom_input):
    # Créer un client fictif pour le test
    client = Client.objects.create(nom_complet='Client Test', email='test@example.com')

    # Créer un commercial fictif pour le test
    commercial = User.objects.create_user(username='testcommercial',
                                          password='testpassword', nom_complet='Test Commercial', role='commercial')

    # Créer un contrat fictif pour le test
    contrat = Contrat.objects.create(client=client, commercial=commercial, montant_total='1000.00',
                                     montant_restant='800.00', statut='En cours')

    # Créer un utilisateur fictif pour le test (rôle: 'gestion')
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='gestion')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='gestion')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=user)

        # Capture de la sortie standard pour vérification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Création d'une instance de la commande
            call_command('delete_contrat', str(contrat.pk))

            # Vérification du message de succès
            assert f"Contrat avec l'ID {contrat.pk} supprimé avec succès" in mock_stdout.write.call_args[0][0]


@pytest.mark.django_db
def test_delete_contrat_not_gestion_team(mocker, custom_input):
    # Créer un client fictif pour le test
    client = Client.objects.create(nom_complet='Client Test', email='test@example.com')

    # Créer un commercial fictif pour le test
    commercial = User.objects.create_user(username='testcommercial',
                                          password='testpassword', nom_complet='Test Commercial', role='commercial')

    # Créer un contrat fictif pour le test
    contrat = Contrat.objects.create(client=client, commercial=commercial, montant_total='1000.00',
                                     montant_restant='800.00', statut='En cours')

    # Créer un utilisateur fictif pour le test (rôle: 'commercial')
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='commercial')

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
        mocker.patch('gestion_client.permissions.validate_token', return_value=user)

        # Capture de la sortie standard pour vérification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Création d'une instance de la commande
            try:
                call_command('delete_contrat', str(contrat.pk))
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == "Vous n'avez pas la permission d'effectuer cette action."


@pytest.mark.django_db
def test_delete_contrat_not_found(mocker, custom_input):
    # Créer un utilisateur fictif pour le test (rôle: 'gestion')
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='gestion')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='gestion')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=user)

        # Capture de la sortie standard pour vérification
        with patch('sys.stderr', new_callable=Mock) as mock_stderr:
            # Création d'une instance de la commande
            try:
                # Utilisation d'un ID qui n'existe pas
                call_command('delete_contrat', '999')
            except CommandError as ce:
                # Vérification du message d'erreur
                assert str(ce) == "Le contrat avec l'ID 999 n'existe pas."
