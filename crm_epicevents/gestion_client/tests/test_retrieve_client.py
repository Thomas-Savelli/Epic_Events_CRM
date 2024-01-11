import pytest
from django.core.management import call_command
from gestion_client.models import Client, User
from django.core.management.base import CommandError
from datetime import datetime, timedelta
from unittest.mock import patch
from io import StringIO
import sys


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_retrieve_client_all_info_connected(mocker):
    # Utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='commercial')

    # Créer des clients fictifs pour le test
    client1 = Client.objects.create(nom_complet='Client A',
                                    email='client_a@example.com', telephone='123456789', entreprise='Entreprise A')
    client2 = Client.objects.create(nom_complet='Client B',
                                    email='client_b@example.com', telephone='987654321', entreprise='Entreprise B')

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

        expected_output = "Listes des Clients\n"

        # Rediriger la sortie standard
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        # Appel de la fonction handle de la commande avec capture de la sortie
        call_command('retrieve_client')

        # Récupération de la sortie standard capturée
        captured_output = sys.stdout.getvalue().strip()

        # Rétablir la sortie standard originale
        sys.stdout = original_stdout

        # Vérification de la sortie standard
        assert expected_output.strip() in captured_output.strip()


@pytest.mark.django_db
def test_retrieve_client_with_details(mocker):
    # Utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='commercial')

    # Créer des clients fictifs pour le test
    client1 = Client.objects.create(nom_complet='Client A', email='client_a@example.com',
                                    telephone='123456789', entreprise='Entreprise A')
    client2 = Client.objects.create(nom_complet='Client B', email='client_b@example.com',
                                    telephone='987654321', entreprise='Entreprise B')

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

        expected_output1 = "Listes des Clients\n"
        expected_output2 = "Listes des Clients\n"

        # Rediriger la sortie standard
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        # Appel de la fonction handle de la commande avec capture de la sortie pour la première recherche
        call_command('retrieve_client', '--nom_complet', 'Client A')
        # Récupération de la sortie standard capturée
        captured_output1 = sys.stdout.getvalue().strip()

        # Appel de la fonction handle de la commande avec capture de la sortie pour la deuxième recherche
        call_command('retrieve_client', '--email', 'client_b@example.com')
        # Récupération de la sortie standard capturée
        captured_output2 = sys.stdout.getvalue().strip()

        # Rétablir la sortie standard originale
        sys.stdout = original_stdout

        # Vérification de la sortie standard pour la première recherche
        assert expected_output1.strip() in captured_output1.strip()

        # Vérification de la sortie standard pour la deuxième recherche
        assert expected_output2.strip() in captured_output2.strip()


@pytest.mark.django_db
def test_retrieve_client_unauthenticated_user(mocker):
    # Créer un utilisateur fictif qui n'est pas connecté
    user = User.objects.create_user(username='unauthenticated_user', password='testpassword')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value=None)

        # Mock de la fonction load_token pour retourner un token invalide
        mocker.patch('gestion_client.permissions.load_token', return_value=None)

        expected_output = "L'utilisateur n'est pas connecté. Veuillez vous connecter."

        # Rediriger la sortie standard
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        try:
            # Appel de la fonction handle de la commande avec capture de la sortie
            call_command('retrieve_client', '--nom_complet', 'Client A')
        except CommandError as e:
            # Capturer l'erreur et vérifier si elle correspond à ce qui est attendu
            assert str(e) == expected_output
