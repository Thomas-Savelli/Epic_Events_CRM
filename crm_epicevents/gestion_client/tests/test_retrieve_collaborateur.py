import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from gestion_client.models import User
from datetime import datetime, timedelta
from unittest.mock import patch
from io import StringIO
import sys


@pytest.fixture
def custom_input():
    return lambda _: "testpassword"


@pytest.mark.django_db
def test_retrieve_collaborateur_connected_user(mocker):
    # Créer un utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='gestion')

    # Mock de la fonction getpass pour éviter les demandes de mot de passe réelles
    mocker.patch('getpass.getpass', return_value='testpassword')

    # Utilisation de patch pour simuler l'entrée utilisateur
    with patch('builtins.input', side_effect=custom_input):
        # Mock pour contourner la vérification de l'autorisation
        mocker.patch('gestion_client.permissions.get_user_role_from_token', return_value='admin')

        # Mock de la fonction load_token pour retourner un token valide
        mocker.patch('gestion_client.permissions.load_token',
                     return_value=('test_token', datetime.utcnow() + timedelta(days=1)))

        # Mock de la fonction validate_token pour retourner un utilisateur valide
        mocker.patch('gestion_client.permissions.validate_token', return_value=user)

        expected_output = "Listes des Collaborateurs\n"

        # Rediriger la sortie standard
        original_stdout = StringIO()
        sys.stdout = original_stdout

        # Appel de la fonction handle de la commande avec capture de la sortie
        call_command('retrieve_collaborateur')

        # Récupération de la sortie standard capturée
        captured_output = original_stdout.getvalue().strip()

        # Rétablir la sortie standard originale
        sys.stdout = sys.__stdout__

        # Vérification de la sortie standard
        assert expected_output.strip() in captured_output.strip()


@pytest.mark.django_db
def test_retrieve_collaborateur_with_filters(mocker):
    # Utilisateur fictif pour le test
    user = User.objects.create_user(username='testuser', password='testpassword',
                                    nom_complet='Test User', role='commercial')

    # Créer des clients fictifs pour le test
    collaborateur1 = User.objects.create(nom_complet='Collaborateur A', role='support',
                                         username='collabA')
    collaborateur2 = User.objects.create(nom_complet='Collaborateur B', role='commercial',
                                         username='collabB')

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

        expected_output1 = "Listes des Collaborateurs\n"
        expected_output2 = "Listes des Collaborateurs\n"

        # Rediriger la sortie standard
        original_stdout = sys.stdout
        sys.stdout = StringIO()

        # Appel de la fonction handle de la commande avec capture de la sortie pour la première recherche
        call_command('retrieve_collaborateur', '--nom_complet', 'Collaborateur A')
        # Récupération de la sortie standard capturée
        captured_output1 = sys.stdout.getvalue().strip()

        # Appel de la fonction handle de la commande avec capture de la sortie pour la deuxième recherche
        call_command('retrieve_collaborateur', '--username', 'collabB')
        # Récupération de la sortie standard capturée
        captured_output2 = sys.stdout.getvalue().strip()

        # Rétablir la sortie standard originale
        sys.stdout = original_stdout

        # Vérification de la sortie standard pour la première recherche
        assert expected_output1.strip() in captured_output1.strip()
        assert "Collaborateur A" in captured_output1
        assert "Support" in captured_output1

        # Vérification de la sortie standard pour la deuxième recherche
        assert expected_output2.strip() in captured_output2.strip()
        assert "Collaborateur B" in captured_output2
        assert "Commercial" in captured_output2


@pytest.mark.django_db
def test_retrieve_collaborateur_unauthenticated_user(mocker):
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
            call_command('retrieve_collaborateur')
        except CommandError as e:
            # Capturer l'erreur et vérifier si elle correspond à ce qui est attendu
            assert str(e) == expected_output
