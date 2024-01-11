import pytest
from django.core.management import call_command
from gestion_client.models import User
from gestion_client.management.commands.create_client import Command
from unittest.mock import patch, Mock
from datetime import datetime, timedelta
from django.core.management.base import CommandError


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_create_client_success(mocker, custom_input):
    # Utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='commercial')

    # Donnée de sortie attendues pour le test
    expected_output = "Client 'Test Client' créé avec succès. ID du client : 1"

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='commercial')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token', return_value=('test_token',
                                                                            datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=user)

        # Capture de la sortie standard pour vérification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Création d'une instance de la commande
            cmd = Command()

            # Appel de la fonction handle de la commande
            call_command('create_client', 'Test Client', 'testclient@example.com',
                         '123456789', 'Test Company', '--date_derniere_maj=2024-01-15 12:00:00')

            # Vérification de la sortie standard
            assert expected_output in mock_stdout.write.call_args[0][0]


@pytest.mark.django_db
def test_create_client_permission_failure(mocker, custom_input):
    # Création d'un utilisateur fictif pour le test avec le rôle approprié
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='gestion')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Mock de la création de l'utilisateur dans la base de données
    mocker.patch('gestion_client.models.User.objects.create_user', return_value=user)

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='gestion')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token',
                     return_value=User.objects.create_user(username='testuser', role='gestion'))

        # Capture de la sortie standard pour vérification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Création d'une instance de la commande
            cmd = Command()

            # Appel de la fonction handle de la commande
            with pytest.raises(CommandError) as exc_info:
                cmd.handle(nom_complet='Test User', role='gestion', username='testuser', email='testuser@example.com')

            # Vérification du message d'erreur
            assert str(exc_info.value) == "Vous n'avez pas la permission d'effectuer cette action."


@pytest.mark.django_db
def test_create_client_not_connected(mocker, custom_input):
    # Utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='gestion')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Mock de la création de l'utilisateur dans la base de données
    mocker.patch('gestion_client.models.User.objects.create_user', return_value=user)

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock de la fonction load_token pour retourner None (utilisateur non connecté)
        mocker.patch('gestion_client.permissions.load_token', return_value=None)

        # Capture de la sortie standard pour vérification
        with patch('sys.stdout', new_callable=Mock) as mock_stdout:
            # Création d'une instance de la commande
            cmd = Command()

            # Appel de la fonction handle de la commande sans utilisateur connecté
            with pytest.raises(CommandError) as exc_info:
                cmd.handle(nom_complet='Test User', role='gestion', username='testuser', email='testuser@example.com')

            # Vérification du message d'erreur
            assert str(exc_info.value) == "L'utilisateur n'est pas connecté. Veuillez vous connecter."
